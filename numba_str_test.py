#! /usr/bin/env python
import binascii
import math
import secrets
from functools import reduce
from timeit import default_timer as time

import camellia
import numpy as np
from numba import cuda

ELEM = 2000
DIM = (1, 1)
MOD = 2 ** 32 - 1

KEY = b'kchdgbdgfncjsgdj'
IV = b'odjdnfhcbsghdbcy'


def set_dim(n):
    global DIM
    assert(n < 1000**2)
    s = int(math.sqrt(n))
    while s > 0:
        if n % s == 0:
            DIM = (s, n // s)
            break
        s -= 1
        assert(n // s < 1000)
    assert(reduce(lambda a, b: a*b, DIM) == n)


def hash(s):
    h = 0

    for i in s:
        h = (i + (h << 6) + (h << 16) - h) % MOD

    return np.uint32(h)


@cuda.jit('void(u4[:], u4, i4[:])')
def str_kernel(arr, s, res):
    pos = cuda.grid(1)
    if pos < ELEM:
        if arr[pos] == s:
            cuda.atomic.compare_and_swap(res, 0, pos)


set_dim(ELEM)

c1 = camellia.new(key=KEY, IV=IV, mode=camellia.MODE_CFB)

arr = [c1.encrypt(secrets.token_bytes()) for _ in range(ELEM)]
np_arr = np.array([hash(x) for x in arr])
assert (reduce(lambda a, b: a*b, DIM) == np_arr.shape[0])
assert (np_arr.dtype == np.uint32)

stream = cuda.stream()
dA = cuda.to_device(np_arr, stream)

st = arr[secrets.randbelow(len(arr))]
h_st = hash(st)

np_res = np.zeros(1, dtype=np.int32)
dC = cuda.to_device(np_res, stream)

stream.synchronize()

s = time()

with stream.auto_synchronize():
    str_kernel[DIM[0], DIM[1]](dA, h_st, dC)
    dC.to_host(stream)

e = time()

v1 = binascii.hexlify(camellia.new(key=KEY, IV=IV, mode=camellia.MODE_CFB).decrypt(arr[np_res[0]])).decode('utf-8')
v2 = binascii.hexlify(camellia.new(key=KEY, IV=IV, mode=camellia.MODE_CFB).decrypt(st)).decode('utf-8')

assert(v1 == v2)
print('cuda: {0:1.6f}'.format(e - s))
print("{0} = {1}".format(v1, v2))
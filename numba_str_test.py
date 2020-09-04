#! /usr/bin/env python
import binascii
import math
import string
from functools import reduce
from timeit import default_timer as time

import camellia
import numpy as np
from numba import cuda

import MT19937

ELEM = 2000
DIM = (1, 1)
MOD = 2 ** 64 - 1


def get_bytes(n=16, ascii=string.ascii_letters):
    return bytes("".join([ascii[MT19937.genrand() % len(ascii)] for _ in range(n)]), 'utf-8')


def set_dim(n):
    global DIM
    LIM = 1000
    VEC = 10
    assert(0 < n < LIM**2)
    if n < VEC**2:
        DIM = (1, n)
        return

    h = math.isqrt(n)
    _x = 1
    _xx = h
    for i in reversed(range(h-VEC, h)):
        _m = n % i
        if _m == 0:
            _x = i
            break
        elif _m < _xx:
            _x = i
            _xx = _m

    DIM = (_x, math.ceil(n / _x))
    assert(reduce(lambda a, b: a*b, DIM) >= n)
    assert(reduce(lambda a, b: a+b, DIM) < LIM*2+VEC)


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

KEY = get_bytes(16)
IV = get_bytes(16)

c1 = camellia.new(key=KEY, IV=IV, mode=camellia.MODE_CFB)

MT19937.sgenrand(4357)

arr = [c1.encrypt(get_bytes(32)) for _ in range(ELEM)]
np_arr = np.array([hash(x) for x in arr])
assert (reduce(lambda a, b: a*b, DIM) >= np_arr.shape[0])
assert (np_arr.dtype == np.uint32)

stream = cuda.stream()
dA = cuda.to_device(np_arr, stream)

MT19937.sgenrand(math.floor(time()))

st = arr[MT19937.genrand() % (len(arr))]
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

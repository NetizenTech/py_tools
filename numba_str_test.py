#! /usr/bin/env python
import math
import os
import string
from functools import reduce
from timeit import default_timer as time

import camellia
import numpy as np
from numba import cuda
from rdrand import *

ELEM = 20_000
DIM = (1, 1)


def get_bytes(n=16, ascii=string.ascii_letters):
    # return bytes("".join([ascii[rand16() % len(ascii)] for _ in range(n)]), 'utf-8')
    return os.urandom(n)


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


def hash0(s):
    assert(type(s) == bytes)
    assert(0 < len(s) < 1000)
    x = 0

    for i in s:
        x ^= i
        x ^= (x >> 29) & 0x5555555555555555
        x ^= (x << 17) & 0x71D67FFFEDA60000
        x ^= (x << 37) & 0xFFF7EEE000000000
        x ^= (x >> 43)

    return np.uint64(x)


@cuda.jit('void(u8[:], u8, i4[:])')
def str_kernel(arr, s, res):
    pos = cuda.grid(1)
    if pos < ELEM:
        if arr[pos] == s:
            # cuda.atomic.compare_and_swap(res, 0, pos)
            idx = cuda.atomic.add(res, 0, 1) + 1
            if idx < len(res):
                res[idx] = pos


set_dim(ELEM)

KEY = get_bytes(16)
IV = get_bytes(16)

c1 = camellia.new(key=KEY, IV=IV, mode=camellia.MODE_ECB)

arr = [c1.encrypt(get_bytes(32)) for _ in range(ELEM)]
np_arr = np.array([hash0(x) for x in arr])
assert (reduce(lambda a, b: a*b, DIM) >= np_arr.shape[0])
assert (np_arr.dtype == np.uint64)

stream = cuda.stream()
dA = cuda.to_device(np_arr, stream)

st = arr[rand16() % (len(arr))]
h_st = hash0(st)

np_res = np.zeros(10, dtype=np.int32)
dC = cuda.to_device(np_res, stream)

stream.synchronize()

s = time()

with stream.auto_synchronize():
    str_kernel[DIM[0], DIM[1]](dA, h_st, dC)
    dC.to_host(stream)

e = time()

v1 = c1.decrypt(arr[np_res[1]]).hex()
v2 = c1.decrypt(st).hex()

assert(v1 == v2)
print('cuda:\t\t\t\t {0:1.6f}s'.format(e - s))
print("Total GPU search results:\t {0:,d} of {1:,d}".format(np_res[0], ELEM))
print("{0} = {1}".format(v1, v2))

#! /usr/bin/env python
import secrets
from timeit import default_timer as time

import numpy as np
from numba import cuda

E = 2000
DIM = (40, 50)
M = 2 ** 32


def hash(s):  # <=>
    h = 0

    for i in bytearray(s, 'utf-8'):
        h = (i + (h << 6) + (h << 16) - h) % M

    return np.uint32(h)


@cuda.jit('void(u4[:], u4, i4[:])')
def str_kernel(arr, s, res):
    pos = cuda.grid(1)
    if pos < E:
        if arr[pos] == s:
            cuda.atomic.compare_and_swap(res, 0, pos)


arr = [secrets.token_hex() for _ in range(E)]
np_arr = np.array([hash(x) for x in arr])
assert (DIM[0] * DIM[1] == np_arr.shape[0])
assert (np_arr.dtype == np.uint32)

stream = cuda.stream()
dA = cuda.to_device(np_arr, stream)

st = arr[secrets.randbelow(len(arr))]
h_st = hash(st)

np_res = np.zeros(1, dtype=np.int32)
dC = cuda.to_device(np_res, stream)

s = time()

with stream.auto_synchronize():
    str_kernel[DIM[0], DIM[1]](dA, h_st, dC)
    dC.to_host(stream)

e = time()

print('cuda: {0:1.6f}'.format(e - s))
print('{0} = {1}'.format(arr[np_res[0]], st))

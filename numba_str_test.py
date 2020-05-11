#! /usr/bin/env python
import math
import secrets
from timeit import default_timer as time

import numpy as np
from numba import cuda


@cuda.jit('void(i1[:,:], i1[:], i4[:])')
def str_kernel(arr, s, res):
    pos = cuda.grid(1)
    size = arr[pos].size
    if size != s.size:
        return
    for i in range(size):
        if arr[pos][i] != s[i]:
            return
    cuda.atomic.compare_and_swap(res, 0, pos)


arr = [secrets.token_hex() for _ in range(2048)]
np_arr = np.array(list(map(lambda x: np.byte(bytearray(x, 'utf-8')), arr)))

threadsperblock = min(1024, np_arr.shape[0])
blockspergrid = min(1024, math.ceil(np_arr.shape[0] / threadsperblock))
assert (threadsperblock * blockspergrid == np_arr.shape[0])

stream = cuda.stream()
dA = cuda.to_device(np_arr, stream)
dB = cuda.device_array(len(np_arr[0]), np_arr.dtype, stream=stream)

st = arr[secrets.randbelow(len(arr))]
np_st = np.byte(bytearray(st, 'utf-8'))

np_res = np.zeros(1, dtype=np.int32)
dC = cuda.to_device(np_res, stream)

s = time()

with stream.auto_synchronize():
    cuda.to_device(np_st, stream, to=dB)
    str_kernel[blockspergrid, threadsperblock](dA, dB, dC)
    dC.to_host(stream)

e = time()

print('cuda: {0:1.6f}'.format(e - s))
print('{0} == {1}'.format(arr[np_res[0]], st))

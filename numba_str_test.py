#! /usr/bin/env numba
import camellia
import numba
import numpy as np
from numba import cuda

assert(cuda.is_available())

ELEM = 20_000
DIM = (1, 1)


def set_dim(n):
    global DIM
    LIM = 1000
    VEC = 10
    assert(0 < n < LIM**2)
    if n < VEC**2:
        DIM = (1, n)
        return

    h = int(np.sqrt(n))
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

    DIM = (_x, int(np.ceil(n / _x)))
    assert(np.prod(DIM) >= n)
    assert(np.sum(DIM) < LIM*2+VEC)


# hash
def hash0(s):
    x = 0

    for i in s:
        x ^= i
        x ^= (x >> 29) & 0x5555555555555555
        x ^= (x << 17) & 0x71D67FFFEDA60000
        x ^= (x << 37) & 0xFFF7EEE000000000
        x ^= (x >> 43)

    return x


c_hash0 = numba.njit('u8(u1[:])')(hash0)

d_hash0 = cuda.jit('u8(u1[:])', device=True)(hash0)


# kernels
@cuda.jit('void(u1[:,:], u8[:])')
def hash0_kernel(s_arr, h_arr):
    pos = cuda.grid(1)
    if pos < h_arr.shape[0]:
        h_arr[pos] = d_hash0(s_arr[pos])


@cuda.jit('void(u8[:], u8, i4[:])')
def search_kernel(h_arr, h, r_arr):
    pos = cuda.grid(1)
    if pos < h_arr.shape[0]:
        if h_arr[pos] == h:
            # cuda.atomic.compare_and_swap(res, 0, pos)
            idx = cuda.atomic.add(r_arr, 0, 1) + 1
            if idx < r_arr.shape[0]:
                r_arr[idx] = pos


c_ecb = camellia.new(key=np.random.bytes(24), mode=camellia.MODE_ECB)

np_str = np.array([bytearray(c_ecb.encrypt(np.random.bytes(32))) for _ in range(ELEM)], dtype=np.uint8)

stream = cuda.stream()

dEX = cuda.to_device(np_str, stream)
dHH = cuda.device_array(np_str.shape[0], dtype=np.uint64)
dRR = cuda.device_array(10, dtype=np.int32)

r_str = np_str[np.random.randint(np_str.shape[0])]
h_str = c_hash0(r_str)

set_dim(np_str.shape[0])
stream.synchronize()

hash0_kernel[DIM](dEX, dHH)

search_kernel[DIM](dHH, h_str, dRR)

np_res = dRR.copy_to_host()

v1 = c_ecb.decrypt(bytes(np_str[np_res[1]])).hex()
v2 = c_ecb.decrypt(bytes(r_str)).hex()

assert(v1 == v2)
print("Total GPU search results:\t {0:,d} of {1:,d}".format(np_res[0], np_str.shape[0]))
print("{0} = {1}".format(v1, v2))

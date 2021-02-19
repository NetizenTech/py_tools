#! /usr/bin/env python
"""Python interface for RNG (Cryptographic Co-Processor). Coded by Wojciech Lawren."""
from cffi import FFI

src = """
uint64_t rand64(void);

uint32_t rand32(void);

uint16_t rand16(void);

uint64_t seed64(void);

uint32_t seed32(void);

uint16_t seed16(void);

void rand_bytes(uint8_t *r, const uint16_t N);
"""
ffi = FFI()
ffi.cdef(src)
lib = ffi.dlopen("librdrand.so")


def rand64():
    return int(lib.rand64())


def rand32():
    return int(lib.rand32())


def rand16():
    return int(lib.rand16())


def seed64():
    return int(lib.seed64())


def seed32():
    return int(lib.seed32())


def seed16():
    return int(lib.seed16())


def rand_bytes(n):
    assert(0 < n < 2 ** 16 and n % 4 == 0)
    x = ffi.new("uint8_t[{0:d}]".format(n))
    lib.rand_bytes(x, n)
    return bytes(x)


if __name__ == "__main__":

    from timeit import default_timer as time

    N = 100_000
    NN = N // 100
    NB = 64

    for f in (rand64, rand32, rand16, seed64, seed32, seed16):
        s = time()
        for i in range(N):
            x = f()
        e = time()
        print("{0}:\t{3:,d}(loops)\t{1:.6f}\t\t{2:d}".format(f.__name__, (e - s), x, N))

    s = time()
    for i in range(NN):
        x = rand_bytes(NB)
    e = time()
    print(x.hex())
    print("rand_bytes[{2:d}]:\t{1:,d}(loops)\t{0:.6f}".format((e - s), NN, NB))

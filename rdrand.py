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

void rand_bytes(uint8_t *r, const uint32_t n);

void seed_bytes(uint8_t *r, const uint32_t n);
"""
ffi = FFI()
ffi.cdef(src)
lib = ffi.dlopen("librdrand.so")

MAX_BYTES = 2 ** 22
DEFAULT_N = 32


def rand64() -> int:
    return int(lib.rand64())


def rand32() -> int:
    return int(lib.rand32())


def rand16() -> int:
    return int(lib.rand16())


def seed64() -> int:
    return int(lib.seed64())


def seed32() -> int:
    return int(lib.seed32())


def seed16() -> int:
    return int(lib.seed16())


def rand_bytes(n: int = DEFAULT_N) -> bytes:
    assert(0 < n < MAX_BYTES and n % 8 == 0)
    x = ffi.new("uint8_t[{0:d}]".format(n))
    lib.rand_bytes(x, n)
    return bytes(ffi.buffer(x, n))


def seed_bytes(n: int = DEFAULT_N) -> bytes:
    assert(0 < n < MAX_BYTES and n % 8 == 0)
    x = ffi.new("uint8_t[{0:d}]".format(n))
    lib.seed_bytes(x, n)
    return bytes(ffi.buffer(x, n))


# TESTS
RDS = 100
ITR = 1_000


def test_rand64(benchmark):
    benchmark.pedantic(rand64, rounds=RDS, iterations=ITR)


def test_rand32(benchmark):
    benchmark.pedantic(rand32, rounds=RDS, iterations=ITR)


def test_rand16(benchmark):
    benchmark.pedantic(rand16, rounds=RDS, iterations=ITR)


def test_seed64(benchmark):
    benchmark.pedantic(seed64, rounds=RDS, iterations=ITR)


def test_seed32(benchmark):
    benchmark.pedantic(seed32, rounds=RDS, iterations=ITR)


def test_seed16(benchmark):
    benchmark.pedantic(seed16, rounds=RDS, iterations=ITR)


def test_rand_bytes(benchmark):
    benchmark.pedantic(rand_bytes, rounds=(RDS // 10), iterations=ITR)


def test_seed_bytes(benchmark):
    benchmark.pedantic(seed_bytes, rounds=(RDS // 10), iterations=ITR)

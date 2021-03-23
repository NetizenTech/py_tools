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
"""
ffi = FFI()
ffi.cdef(src)
lib = ffi.dlopen("librdrand.so")

MAX_BITS = 2 ** 12
DEFAULT_Z = 251
MAX_BYTES = 2 ** 22
DEFAULT_N = 32
BYTEORDER = "big"


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


def rand_bigint(n: int = DEFAULT_Z) -> int:
    assert(64 < n < MAX_BITS)
    string = str()
    while len(string) < n:
        string += bin(rand64())[2:]
    return int(string[:n], 2)


def seed_bigint(n: int = DEFAULT_Z) -> int:
    assert(64 < n < MAX_BITS)
    string = str()
    while len(string) < n:
        string += bin(seed64())[2:]
    return int(string[:n], 2)


def rand_bytes(n: int = DEFAULT_N) -> bytes:
    assert(1 < n < MAX_BYTES)
    string = bytes()
    if n < 8:
        for _ in range(sum(divmod(n, 2))):
            string += rand16().to_bytes(2, BYTEORDER)
        return string[:n]

    (q, r) = divmod(n, 8)
    if r > 0:
        q += 1
    for _ in range(q):
        string += rand64().to_bytes(8, BYTEORDER)
    return string[:n]


def seed_bytes(n: int = DEFAULT_N) -> bytes:
    assert(1 < n < MAX_BYTES)
    string = bytes()
    if n < 8:
        for _ in range(sum(divmod(n, 2))):
            string += seed16().to_bytes(2, BYTEORDER)
        return string[:n]

    (q, r) = divmod(n, 8)
    if r > 0:
        q += 1
    for _ in range(q):
        string += seed64().to_bytes(8, BYTEORDER)
    return string[:n]


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


def test_r_bigint(benchmark):
    benchmark.pedantic(rand_bigint, rounds=RDS, iterations=ITR)


def test_s_bigint(benchmark):
    benchmark.pedantic(seed_bigint, rounds=RDS, iterations=ITR)


def test_rand_bytes(benchmark):
    benchmark.pedantic(rand_bytes, rounds=(RDS // 10), iterations=ITR)


def test_seed_bytes(benchmark):
    benchmark.pedantic(seed_bytes, rounds=(RDS // 10), iterations=ITR)

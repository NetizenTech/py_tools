#! /usr/bin/env python
"""Python interface for RNG (Cryptographic Co-Processor). Coded by Wojciech Lawren."""
from _rdrand import lib

try:
    import gmpy2 as gmp

    GMP_LIMB_BITS = gmp.mp_limbsize()
    assert(GMP_LIMB_BITS == 64)
    MAX_MPZ = 64
    DEFAULT_Z = 4
except (ImportError, AssertionError):
    GMP_LIMB_BITS = False

MAX_BITS = 2 ** 12
DEFAULT_S = 251

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


if GMP_LIMB_BITS:
    def rand_mpz(n: int = DEFAULT_Z) -> gmp.mpz:
        assert(1 < n < MAX_MPZ)
        return gmp.pack([rand64() for _ in range(n)], GMP_LIMB_BITS)

    def seed_mpz(n: int = DEFAULT_Z) -> gmp.mpz:
        assert(1 < n < MAX_MPZ)
        return gmp.pack([seed64() for _ in range(n)], GMP_LIMB_BITS)


def rand_bigint(n: int = DEFAULT_S) -> int:
    assert(64 < n < MAX_BITS)
    string = str()
    while len(string) < n:
        string += bin(rand64())[2:]
    return int(string[:n], 2)


def seed_bigint(n: int = DEFAULT_S) -> int:
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
RDS = 12
ITR = 250


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


if GMP_LIMB_BITS:
    def test_rand_mpz(benchmark):
        benchmark.pedantic(rand_mpz, rounds=(RDS // 4), iterations=ITR)

    def test_seed_mpz(benchmark):
        benchmark.pedantic(seed_mpz, rounds=(RDS // 4), iterations=ITR)


def test_r_bigint(benchmark):
    benchmark.pedantic(rand_bigint, rounds=(RDS // 4), iterations=ITR)


def test_s_bigint(benchmark):
    benchmark.pedantic(seed_bigint, rounds=(RDS // 4), iterations=ITR)


def test_rand_bytes(benchmark):
    benchmark.pedantic(rand_bytes, rounds=(RDS // 4), iterations=ITR)


def test_seed_bytes(benchmark):
    benchmark.pedantic(seed_bytes, rounds=(RDS // 4), iterations=ITR)

#! /usr/bin/env python
"""Python interface for RNG (Cryptographic Co-Processor). Coded by Wojciech Lawren."""
from _rdrand import lib

MAX_BITS = 2 ** 16
DEFAULT_S = 251

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


def rand_bits(n: int = DEFAULT_S, ef: str = "b", f: str = "064b") -> str:
    assert(64 < n < MAX_BITS)
    string = format(rand64(), ef)
    while len(string) < n:
        string += format(rand64(), f)
    return string[:n]


def seed_bits(n: int = DEFAULT_S, ef: str = "b", f: str = "064b") -> str:
    assert(64 < n < MAX_BITS)
    string = format(seed64(), ef)
    while len(string) < n:
        string += format(seed64(), f)
    return string[:n]


def rand_bytes(n: int = DEFAULT_N, o: str = "big") -> bytes:
    assert(1 < n < MAX_BYTES)
    string = bytes()
    if n < 8:
        for _ in range(sum(divmod(n, 2))):
            string += rand16().to_bytes(2, o)
        return string[:n]

    (q, r) = divmod(n, 8)
    if r > 0:
        q += 1
    for _ in range(q):
        string += rand64().to_bytes(8, o)
    return string[:n]


def seed_bytes(n: int = DEFAULT_N, o: str = "big") -> bytes:
    assert(1 < n < MAX_BYTES)
    string = bytes()
    if n < 8:
        for _ in range(sum(divmod(n, 2))):
            string += seed16().to_bytes(2, o)
        return string[:n]

    (q, r) = divmod(n, 8)
    if r > 0:
        q += 1
    for _ in range(q):
        string += seed64().to_bytes(8, o)
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


def test_rand_bits(benchmark):
    benchmark.pedantic(rand_bits, rounds=(RDS // 4), iterations=ITR)


def test_seed_bits(benchmark):
    benchmark.pedantic(seed_bits, rounds=(RDS // 4), iterations=ITR)


def test_rand_bytes(benchmark):
    benchmark.pedantic(rand_bytes, rounds=(RDS // 4), iterations=ITR)


def test_seed_bytes(benchmark):
    benchmark.pedantic(seed_bytes, rounds=(RDS // 4), iterations=ITR)

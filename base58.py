#! /usr/bin/env python
"""Python implementation of Base58 and Base58Check standards. Coded by Wojciech Lawren."""
from hashlib import sha256

B58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


class Base58Error(Exception):
    """Base58 and Base58Check encoding errors"""


def double_sha256(s: bytes) -> bytes:
    return sha256(sha256(s).digest()).digest()


def int_to_bytes(i: int, o: str = "big") -> bytes:
    return i.to_bytes(max((i.bit_length() + 7) // 8, 1), o)


def b58encode_int(n: int, pad: int = 0) -> str:
    """Encode int to base58 string"""
    ec = []
    while n > 0:
        n, r = divmod(n, 58)
        ec.append(B58_ALPHABET[r])

    encoded = "".join(ec[::-1])
    return B58_ALPHABET[0] * pad + encoded


def b58encode(s: bytes) -> str:
    """Encode bytes to base58 string"""
    n = int.from_bytes(s, "big")
    pad = 0
    for c in s:
        if c == 0:
            pad += 1
        else:
            break

    return b58encode_int(n, pad)


def b58decode_int(s: str) -> int:
    """Decode base58-encoded string to int"""
    n = 0
    for c in s:
        n *= 58
        i = B58_ALPHABET.find(c)
        if i < 0:
            raise Base58Error("{0} not in B58_ALPHABET ({1})".format(c, s))
        n += i

    return n


def b58decode(s: str) -> bytes:
    """Decode base58-encoded string to bytes"""
    decoded = int_to_bytes(b58decode_int(s))

    pad = 0
    for c in s[:-1]:
        if c == B58_ALPHABET[0]:
            pad += 1
        else:
            break

    return b'\x00' * pad + decoded


def b58encode_check(s: bytes, v: int) -> str:
    """Encode bytes and version to a base58check string"""
    sv = int_to_bytes(v) + s
    return b58encode(sv + double_sha256(sv)[:4])


def b58decode_check(s: str, v: int) -> bytes:
    """Decode and check base58check string to bytes"""
    vb = int_to_bytes(v)
    sd = b58decode(s)
    if len(sd) <= (len(vb) + 4):
        raise Base58Error("{} string length fails".format(s))
    if sd[:len(vb)] != vb:
        raise Base58Error("{:d} version check fails".format(v))
    if double_sha256(sd[:-4])[:4] != sd[-4:]:
        raise Base58Error("{} double_sha256 check fails".format(s))
    return sd[len(vb):-4]


# TESTS
RDS = 10
ITR = 100
VERSION = 0x0


def test_b58encint_bench(benchmark):
    benchmark.pedantic(b58encode_int, args=(9876543210,), rounds=RDS, iterations=ITR)


def test_b58decint_bench(benchmark):
    benchmark.pedantic(b58decode_int, args=("2t6V2H",), rounds=RDS, iterations=ITR)


def test_b58encode_bench(benchmark):
    benchmark.pedantic(b58encode, args=(b"Hello World!",), rounds=RDS, iterations=ITR)


def test_b58decode_bench(benchmark):
    benchmark.pedantic(b58decode, args=("19wWTEnNTUzJGD7cXy4XXZX",), rounds=RDS, iterations=ITR)


def test_b58encode_check_bench(benchmark):
    benchmark.pedantic(b58encode_check, args=(b"Hello World!", VERSION,), rounds=RDS, iterations=ITR)


def test_b58decode_check_bench(benchmark):
    benchmark.pedantic(b58decode_check, args=("19wWTEnNTUzJGD7cXy4XXZX", VERSION,), rounds=RDS, iterations=ITR)


def test_b58encode_int():
    assert(b58encode_int(1234567890) == "2t6V2H")
    assert(b58encode_int(58**5) == "211111")


def test_b58decode_int():
    assert(b58decode_int("2t6V2H") == 1234567890)
    assert(b58decode_int("211111") == 58**5)


def test_b58encode():
    assert(b58encode(b"Hello World!") == "2NEpo7TZRRrLZSi2U")
    assert(b58encode(
        b"The quick brown fox jumps over the lazy dog.") ==
        "USm3fpXnKG5EUBx2ndxBDMPVciP5hGey2Jh4NDv6gmeo1LkMeiKrLJUUBk6Z")


def test_b58decode():
    assert(b58decode("2NEpo7TZRRrLZSi2U") == b"Hello World!")
    assert(b58decode(
        "USm3fpXnKG5EUBx2ndxBDMPVciP5hGey2Jh4NDv6gmeo1LkMeiKrLJUUBk6Z") ==
        b"The quick brown fox jumps over the lazy dog.")


def test_b58encode_check():
    assert(b58encode_check(b"Hello World!", VERSION) == "19wWTEnNTUzJGD7cXy4XXZX")
    assert(b58encode_check(
        b"The quick brown fox jumps over the lazy dog.", VERSION) ==
        "146auvTd4NTVoJhFVnfh9reLsP21HQAQUFXCCBzNZjAPwQBRpaSp4aDLzWajGtiLqw2")
    assert(b58encode_check(bytes.fromhex(
        "f54a5851e9372b87810a8e60cdd2e7cfd80b6e31"), VERSION) ==
        "1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs")


def test_b58decode_check():
    assert(b58decode_check("19wWTEnNTUzJGD7cXy4XXZX", VERSION) == b"Hello World!")
    assert(b58decode_check(
        "146auvTd4NTVoJhFVnfh9reLsP21HQAQUFXCCBzNZjAPwQBRpaSp4aDLzWajGtiLqw2", VERSION) ==
        b"The quick brown fox jumps over the lazy dog.")
    assert(b58decode_check(
        "1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs", VERSION) ==
        bytes.fromhex("f54a5851e9372b87810a8e60cdd2e7cfd80b6e31"))

#! /usr/bin/env python
from cffi import FFI

ffibuilder = FFI()
cdef = """
uint64_t rand64(void);

uint32_t rand32(void);

uint16_t rand16(void);

uint64_t seed64(void);

uint32_t seed32(void);

uint16_t seed16(void);
"""
ffibuilder.cdef(cdef)

src = str()

with open("rdrand.h", "r") as h:
    src += h.read()
with open("rdrand.c", "r") as c:
    src += c.read()

ffibuilder.set_source("_rdrand", src)

if __name__ == "__main__":
    ffibuilder.compile()

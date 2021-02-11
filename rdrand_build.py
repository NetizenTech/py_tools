#! /usr/bin/env python
from cffi import FFI

src = """
uint64_t _rand64(void);

uint32_t _rand32(void);

uint16_t _rand16(void);

uint64_t _seed64(void);

uint32_t _seed32(void);

uint16_t _seed16(void);
"""

ffibuilder = FFI()
ffibuilder.cdef(src)
ffibuilder.set_source(
    "_rdrand",
    src,
    sources=["rdrand.c"],
    libraries=[]
)

if __name__ == "__main__":
    ffibuilder.compile()

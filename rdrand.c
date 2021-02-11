#include "rdrand.h"

#define LOOP 10

#define RAND "rdrand %0\n\t"
#define SEED "rdseed %0\n\t"

#define RD(i)                                                                                                          \
    asm volatile("mov %1, %%ecx\n\t"                                                                                   \
                 "1:\n\t" i "jc 2f\n\t"                                                                                \
                 "loop 1b\n\t"                                                                                         \
                 "xor %0, %0\n\t"                                                                                      \
                 "2:"                                                                                                  \
                 : "=r"(v)                                                                                             \
                 : "n"(LOOP)                                                                                           \
                 : "rcx", "cc")

uint64_t _rand64()
{
    register uint64_t v asm("rax");
    RD(RAND);
    return v;
}

uint32_t _rand32()
{
    register uint32_t v asm("eax");
    RD(RAND);
    return v;
}

uint16_t _rand16()
{
    register uint16_t v asm("ax");
    RD(RAND);
    return v;
}

uint64_t _seed64()
{
    register uint64_t v asm("rax");
    RD(SEED);
    return v;
}

uint32_t _seed32()
{
    register uint32_t v asm("eax");
    RD(SEED);
    return v;
}

uint16_t _seed16()
{
    register uint16_t v asm("ax");
    RD(SEED);
    return v;
}

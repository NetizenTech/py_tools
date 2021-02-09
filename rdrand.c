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

unsigned long _rand64()
{
    register unsigned long v asm("rax");
    RD(RAND);
    return v;
}

unsigned _rand32()
{
    register unsigned v asm("eax");
    RD(RAND);
    return v;
}

unsigned short _rand16()
{
    register unsigned short v asm("ax");
    RD(RAND);
    return v;
}

unsigned long _seed64()
{
    register unsigned long v asm("rax");
    RD(SEED);
    return v;
}

unsigned _seed32()
{
    register unsigned v asm("eax");
    RD(SEED);
    return v;
}

unsigned short _seed16()
{
    register unsigned short v asm("ax");
    RD(SEED);
    return v;
}

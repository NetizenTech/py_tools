#include <assert.h>
#include <stdint.h>

#define RC 10

#define RAND "rdrand %0\n\t"
#define SEED "rdseed %0\n\t"

#define RD(i)                                                                                                          \
    asm volatile("mov %1, %%ecx\n\t"                                                                                   \
                 "1:\n\t" i "jc 2f\n\t"                                                                                \
                 "loop 1b\n\t"                                                                                         \
                 "xor %0, %0\n\t"                                                                                      \
                 "2:"                                                                                                  \
                 : "=r"(v)                                                                                             \
                 : "n"(RC)                                                                                             \
                 : "rcx", "cc")

uint64_t rand64(void) __attribute__((nothrow));

uint32_t rand32(void) __attribute__((nothrow));

uint16_t rand16(void) __attribute__((nothrow));

uint64_t seed64(void) __attribute__((nothrow));

uint32_t seed32(void) __attribute__((nothrow));

uint16_t seed16(void) __attribute__((nothrow));

void rand_bytes(uint8_t *r, const uint16_t N) __attribute__((nonnul));

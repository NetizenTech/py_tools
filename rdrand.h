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

uint64_t rand64(void);

uint32_t rand32(void);

uint16_t rand16(void);

uint64_t seed64(void);

uint32_t seed32(void);

uint16_t seed16(void);

void rand_bytes(uint8_t *r, const uint32_t n) __attribute__((nonnul));

void seed_bytes(uint8_t *r, const uint32_t n) __attribute__((nonnul));

#include <rdrand.h>

uint64_t rand64()
{
    register uint64_t v asm("rax");
    RD(RAND);
    assert(v > 0);
    return v;
}

uint32_t rand32()
{
    register uint32_t v asm("eax");
    RD(RAND);
    assert(v > 0);
    return v;
}

uint16_t rand16()
{
    register uint16_t v asm("ax");
    RD(RAND);
    assert(v > 0);
    return v;
}

uint64_t seed64()
{
    register uint64_t v asm("rax");
    RD(SEED);
    assert(v > 0);
    return v;
}

uint32_t seed32()
{
    register uint32_t v asm("eax");
    RD(SEED);
    assert(v > 0);
    return v;
}

uint16_t seed16()
{
    register uint16_t v asm("ax");
    RD(SEED);
    assert(v > 0);
    return v;
}

void rand_bytes(uint8_t *r, const uint32_t n)
{
    assert(r && n % 8 == 0);
    uint64_t *rb = (uint64_t *)r;

    for (uint32_t i = 0; i < (n / 8); i++)
        rb[i] = rand64();
}

void seed_bytes(uint8_t *r, const uint32_t n)
{
    assert(r && n % 8 == 0);
    uint64_t *rb = (uint64_t *)r;

    for (uint32_t i = 0; i < (n / 8); i++)
        rb[i] = seed64();
}

#include <rdrand.h>

uint64_t rand64()
{
    register uint64_t v asm("rax");
    RD(RAND);
    return v;
}

uint32_t rand32()
{
    register uint32_t v asm("eax");
    RD(RAND);
    return v;
}

uint16_t rand16()
{
    register uint16_t v asm("ax");
    RD(RAND);
    return v;
}

uint64_t seed64()
{
    register uint64_t v asm("rax");
    RD(SEED);
    return v;
}

uint32_t seed32()
{
    register uint32_t v asm("eax");
    RD(SEED);
    return v;
}

uint16_t seed16()
{
    register uint16_t v asm("ax");
    RD(SEED);
    return v;
}

void rand_bytes(uint8_t *r, const uint16_t n)
{
    assert(n % 4 == 0);
    uint32_t *rb = (uint32_t *)r;

    for (uint16_t i = 0; i < (n / 4); i++)
        rb[i] = rand32();
}

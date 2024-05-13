#include <cassert>
#include <iostream>

using namespace std;

using lli = long long;

#define MOD 998244353

int pow_mod(int exp, int base = 2)
{
    assert(exp >= 0);
    if (exp == 0)
    {
        return 1;
    }
    if (exp % 2)
    {
        return (((lli)(base)*pow_mod(exp - 1, base)) % MOD);
    }
    int root = pow_mod(exp / 2, base);
    return (((lli)(root)*root) % MOD);
}

int mod_inv(int x)
{
    assert(x > 0);
    return pow_mod(MOD - 2, x);
}

struct Minteger
{
    int value;

    Minteger(lli value = 0)
    {
        this->value = mod(value);
    }

    int mod(lli value)
    {
        while (value < 0)
        {
            value += MOD;
        }
        return (value % MOD);
    }

    Minteger &operator+=(const Minteger &other)
    {
        value = mod((lli)(value) + other.value);
        return *this;
    }
    Minteger operator+(const Minteger &other)
    {
        return Minteger((lli)(value) + other.value);
    }

    Minteger &operator-=(const Minteger &other)
    {
        value = mod((lli)(value)-other.value);
        return *this;
    }
    Minteger operator-(const Minteger &other)
    {
        return Minteger((lli)(value)-other.value);
    }

    Minteger &operator*=(const Minteger &other)
    {
        value = mod((lli)(value)*other.value);
        return *this;
    }
    Minteger operator*(const Minteger &other)
    {
        return Minteger((lli)(value)*other.value);
    }

    Minteger &operator/=(const Minteger &other)
    {
        value = mod((lli)(value)*mod_inv(other.value));
        return *this;
    }
    Minteger operator/(const Minteger &other)
    {
        return Minteger((lli)(value)*mod_inv(other.value));
    }

    friend ostream &operator<<(ostream &os, const Minteger &mi)
    {
        os << mi.value;
        return os;
    }

    explicit operator bool() const
    {
        return value != 0;
    }
};

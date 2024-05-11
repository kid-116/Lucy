#define lli long long

template <typename T = lli>
struct Minteger
{
    T value;

    Minteger(T value = 0)
    {
        while (value < 0)
        {
            value += MOD;
        }
        this->value = value % MOD;
    }

    Minteger operator+(const Minteger &other)
    {
        return Minteger(value + other.value);
    }
};

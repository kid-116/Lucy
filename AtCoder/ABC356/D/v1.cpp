#include <algorithm>
#include <bitset>
#include <cassert>
#include <cmath>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <vector>

using namespace std;

#define YES "Yes"
#define NO "No"

typedef long long lli;

typedef vector<short> v16;
typedef vector<v16> vv16;
typedef vector<bool> vb;
typedef vector<vb> vvb;
typedef vector<int> v32;
typedef vector<v32> vv32;
typedef vector<lli> v64;
typedef vector<v64> vv64;
typedef vector<char> vc;
typedef vector<vc> vvc;
typedef vector<string> vs;

#define all(vec) vec.begin(), vec.end()

#define MOD 998244353

#define MAX_BITS 60

template <typename T, typename U>
istream &operator>>(istream &is, pair<T, U> &p) {
  is >> p.first >> p.second;
  return is;
}
template <typename T>
istream &operator>>(istream &is, vector<T> &vec) {
  for (T &ele : vec) {
    is >> ele;
  }
  return is;
}

template <typename T>
ostream &operator<<(ostream &os, const vector<T> &vec) {
  for (auto const &ele : vec) {
    os << ele << " ";
  }
  return os;
}
template <typename T, typename U>
ostream &operator<<(ostream &os, const pair<T, U> &p) {
  os << p.second << "(" << p.first << ")" << " ";
  return os;
}

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

int main() {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  lli N, M;
  cin >> N >> M;
  bitset<MAX_BITS> m(M);
  Minteger soln(0);
  for (int i = 0; i < MAX_BITS; i++) {
    if (!m[i]) {
        continue;
    }
    lli pattern_sz = 1ll << (i + 1);
    soln += ((N + 1) / pattern_sz) * (pattern_sz / 2);
    lli rem = (N + 1) % pattern_sz;
    rem -= pattern_sz / 2;
    soln += max(rem, 0ll);
  }
  cout << soln << "\n";
  return 0;
}

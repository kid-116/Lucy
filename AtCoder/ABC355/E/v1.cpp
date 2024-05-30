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

#define lli long long

#define v16 vector<short>
#define vv16 vector<vs>
#define vb vector<bool>
#define vvb vector<vb>
#define v32 vector<int>
#define vv32 vector<vi>
#define v64 vector<lli>
#define vv64 vector<vl>
#define vc vector<char>
#define vvc vector<vc>
#define vs vector<string>

#define all(vec) vec.begin(), vec.end()

#define MOD 100

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

// #define MOD 998244353

int pow_mod(int exp, int base = 2) {
  assert(exp >= 0);
  if (exp == 0) {
    return 1;
  }
  if (exp % 2) {
    return (((lli)(base)*pow_mod(exp - 1, base)) % MOD);
  }
  int root = pow_mod(exp / 2, base);
  return (((lli)(root)*root) % MOD);
}

int mod_inv(int x) {
  assert(x > 0);
  return pow_mod(MOD - 2, x);
}

struct Minteger {
  int value;

  Minteger(lli value = 0) { this->value = mod(value); }

  int mod(lli value) {
    while (value < 0) {
      value += MOD;
    }
    return (value % MOD);
  }

  Minteger &operator+=(const Minteger &other) {
    value = mod((lli)(value) + other.value);
    return *this;
  }
  Minteger operator+(const Minteger &other) {
    return Minteger((lli)(value) + other.value);
  }

  Minteger &operator-=(const Minteger &other) {
    value = mod((lli)(value)-other.value);
    return *this;
  }
  Minteger operator-(const Minteger &other) {
    return Minteger((lli)(value)-other.value);
  }

  Minteger &operator*=(const Minteger &other) {
    value = mod((lli)(value)*other.value);
    return *this;
  }
  Minteger operator*(const Minteger &other) {
    return Minteger((lli)(value)*other.value);
  }

  Minteger &operator/=(const Minteger &other) {
    value = mod((lli)(value)*mod_inv(other.value));
    return *this;
  }
  Minteger operator/(const Minteger &other) {
    return Minteger((lli)(value)*mod_inv(other.value));
  }

  friend ostream &operator<<(ostream &os, const Minteger &mi) {
    os << mi.value;
    return os;
  }

  explicit operator bool() const { return value != 0; }
};

int ask(int i, int j) {
  cout << "? " << i << " " << j << endl;
  int T;
  cin >> T;
  return T;
}

int leftmost_set_bit(int n) {
  int pos = -1;
  while (n) {
    n >>= 1;
    pos++;
  }
  return pos;
}
int leftmost_but_set_bit(int n) {
  int leftmost = leftmost_set_bit(n);
  return leftmost_set_bit(n ^ (1 << leftmost));
}
int rightmost_set_bit(int n) { return leftmost_set_bit(n & -n); }

int main() {
  //   ios_base::sync_with_stdio(0);
  //   cin.tie(0);
  int N;
  int L, R;
  cin >> N >> L >> R;
  R += 1;
  Minteger sum(0);
  while (L < R) {
    int i = leftmost_set_bit(R ^ L);
    int L_right = rightmost_set_bit(L);
    if (L_right != -1 && L_right < i) {
      i = L_right;
    }
    int j = L / (1 << i);
    L += 1 << i;
    assert(i >= 0 && j >= 0 && (1 << i) * (j + 1) <= (1 << N));
    int T = ask(i, j);
    // assert(T != -1);
    sum += T;
  }
  cout << "! " << sum << endl;
  return 0;
}

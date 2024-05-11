#include <algorithm>
#include <bitset>
#include <cassert>
#include <cmath>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <vector>

#define YES "Yes"
#define NO "No"

#define lli long long

#define vs vector<short>
#define vvs vector<vs>
#define vb vector<bool>
#define vvb vector<vb>
#define vi vector<int>
#define vvi vector<vi>
#define vl vector<lli>
#define vvl vector<vvl>

#define all(vec) vec.begin(), vec.end()

#define MOD 998244353

using namespace std;

template <typename T, typename U>
istream &operator>>(istream &is, pair<T, U> &p)
{
    is >> p.first >> p.second;
    return is;
}
template <typename T>
istream &operator>>(istream &is, vector<T> &vec)
{
    for (T &ele : vec)
    {
        is >> ele;
    }
    return is;
}

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

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N;
    cin >> N;
    vi A(N);
    cin >> A;
    lli pow_suf = 0;
    lli suf = 0;
    lli soln = 0;
    for (int i = N - 1; i >= 0; i--)
    {
        suf += A[i];
        pow_suf = pow_suf + pow(10ll, to_string(A[i]).length());
    }
    for (int i = 0; i < N; i++)
    {
        suf -= A[i];
        pow_suf -= pow(10ll, to_string(A[i]).length());
        soln = (soln + (A[i] * (pow_suf % MOD)) % MOD) % MOD;
        soln = (soln + (suf % MOD)) % MOD;
    }
    cout << soln << "\n";
    return 0;
}

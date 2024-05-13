#include <algorithm> //
#include <bitset>    //
#include <cassert>   //
#include <cmath>     //
#include <iostream>  //
#include <map>       //
#include <numeric>   //
#include <set>       //
#include <vector>    //

using namespace std; //

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

template <typename T>
ostream &operator<<(ostream &os, const vector<T> &vec)
{
    for (auto const &ele : vec)
    {
        os << ele << " ";
    }
    return os;
}
template <typename T, typename U>
ostream &operator<<(ostream &os, const pair<T, U> &p)
{
    os << p.second << "(" << p.first << ")" << " ";
    return os;
}

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

struct Solver
{
    int H;
    vvi group;
    vvi left;
    vvi right;
    vi group_id;
    vi pole_pos;
    vector<Minteger> prob;
    Minteger prob_mul = 1;
    int num_zeros;
    vector<int> num_quakes;

    Solver(const vector<int> &X, const int H)
    {
        Solver::H = H;
        group.resize(0);
        group_id.resize(X.size(), -1);
        pole_pos.resize(X.size(), -1);

        vector<pair<int, int>> poles;
        for (int i = 0; i < X.size(); i++)
        {
            poles.push_back({X[i], i});
        }
        sort(all(poles));
        // cout << poles << "\n";
        int prev_pos = -1;
        for (auto const &[pos, id] : poles)
        {
            assert(X[id] == pos);
            if (prev_pos != -1 || group.empty())
            {
                if (pos - prev_pos > H || group.empty())
                {
                    group.push_back({});
                }
            }
            group.back().push_back(id);
            group_id[id] = group.size() - 1;
            pole_pos[id] = group.back().size() - 1;
            prev_pos = pos;
        }
        // for (auto const &g : group)
        // {
        //     cout << g << "\n";
        // }

        prob.resize(group.size());
        num_zeros = group.size();

        num_quakes.resize(group.size(), 0);

        prepare_left();
        prepare_right();
    }

    void prepare_left()
    {
        left.resize(0);
        for (const auto &g : group)
        {
            vi l(g.size(), 0);
            vector<int> stack;
            for (int i = 0; i < g.size(); i++)
            {
                while (!stack.empty() && g[stack.back()] > g[i])
                {
                    stack.pop_back();
                }
                l[i] = stack.size();
                stack.push_back(i);
            }
            left.push_back(l);
        }
    }

    void prepare_right()
    {
        right.resize(0);
        for (const auto &g : group)
        {
            vi r(g.size(), 0);
            vector<int> stack;
            for (int i = g.size() - 1; i >= 0; i--)
            {
                while (!stack.empty() && g[stack.back()] > g[i])
                {
                    stack.pop_back();
                }
                r[i] = stack.size();
                stack.push_back(i);
            }
            right.push_back(r);
        }
    }

    int num_poles()
    {
        return group_id.size();
    }

    void solve()
    {
        for (int i = 0; i < num_poles(); i++)
        {
            const int &gid = group_id[i];
            ++num_quakes[gid];
            const int &ppos = pole_pos[i];
            Minteger ans(Minteger(1) / Minteger(pow_mod(left[gid][ppos] + right[gid][ppos])));
            bool l = ppos > 0 && group[gid][ppos - 1] > i;
            bool r = ppos < group[gid].size() - 1 && group[gid][ppos + 1] > i;
            if (l && r)
            {
                ans *= 0;
            }
            else if (l || r)
            {
                ans /= 2;
            }

            const bool was_zero = !prob[gid];
            if (!was_zero)
            {
                prob_mul = prob_mul / prob[gid];
            }
            prob[gid] = prob[gid] + ans;
            const bool is_zero = !prob[gid];
            if (was_zero && !is_zero)
            {
                --num_zeros;
            }
            if (!was_zero && is_zero)
            {
                ++num_zeros;
            }

            assert(num_zeros >= 0);
            if (num_zeros > 0)
            {
                if (num_zeros == 1 && is_zero)
                {
                }
                else
                {
                    ans = 0;
                }
            }
            ans = ans * prob_mul;
            if (!is_zero)
            {
                prob_mul = prob_mul * prob[gid];
            }

            ans = ans * Minteger(pow_mod(num_poles()));
            cout << ans << " ";
        }
        cout << "\n";
    }
};

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N;
    int H;
    cin >> N >> H;
    vi X(N);
    cin >> X;
    Solver solver(X, H);
    solver.solve();
    for (int i = 0; i < N; i++)
    {
        int gid = solver.group_id[i];
        int ppos = solver.pole_pos[i];
        assert(solver.group[gid][ppos] == i);
    }
    // cout << solver.group_id[112] << "\n";
    // cout << solver.num_zeros << "\n";
    // cout << solver.prob_mul.num.value << "\n";
    return 0;
}

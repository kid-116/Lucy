#include <algorithm>
#include <bitset>   //
#include <cassert>  //
#include <cmath>    //
#include <iostream> //
#include <map>      //
#include <numeric>  //
#include <set>      //
#include <vector>   //

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

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    short N;
    short K;
    cin >> N >> K;
    vs A(N);
    cin >> A;
    for (auto const &ele : A)
    {
        if (ele % K == 0)
        {
            cout << ele / K << " ";
        }
    }
    cout << "\n";
    return 0;
}

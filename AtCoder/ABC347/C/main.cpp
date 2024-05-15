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
    int N;
    int A, B;
    cin >> N >> A >> B;
    vi D(N);
    cin >> D;
    // (D[0] + x) % (A + B) == 0
    // D[0] + x = q*(A + B)
    // x = q*(A + B) - D[0]
    lli x = -D[0];
    while (x < 0)
    {
        x += (A + B);
    }
    bool possible = true;
    int space_right = A - 1;
    for (int i = 1; i < N; i++)
    {
        int day = (D[i] + x) % (A + B);
        if (day >= A)
        {
            int to_shift = (A + B) - day;
            if (to_shift > space_right)
            {
                possible = false;
                break;
            }
            space_right -= to_shift;
            x += to_shift;
        }
        else {
            space_right = min(space_right, A - 1 - day);
        }
    }
    // cout << NO << "\n";
    cout << (possible ? YES : NO) << "\n";
    return 0;
}

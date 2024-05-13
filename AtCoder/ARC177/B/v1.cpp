#include <algorithm> //
#include <bitset> //
#include <cassert> //
#include <cmath> //
#include <iostream> //
#include <map> //
#include <numeric> //
#include <set> //
#include <vector> //

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

using namespace std; //

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

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    short N;
    cin >> N;
    string S;
    cin >> S;
    string soln = "";
    for(int i = S.length() - 1; i >= 0; i--) {
        if(S[i] == '0') {
            continue;
        }
        for(int _ = 0; _ < i + 1; _++) {
            soln.push_back('A');
        }
        for(int _ = 0; _ < i; _++) {
            soln.push_back('B');
        }
    }
    cout << soln.length() << "\n";
    cout << soln << "\n";
    return 0;
}

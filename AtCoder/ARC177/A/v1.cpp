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
    int A, B, C, D, E, F; // 1, 5, 10, 50, 100, 500
    cin >> A >> B >> C >> D >> E >> F;
    map<int, int> wallet;
    wallet[1] = A;
    wallet[5] = B;
    wallet[10] = C;
    wallet[50] = D;
    wallet[100] = E;
    wallet[500] = F;
    int N;
    cin >> N;
    bool is_possible = true;
    while(N--) {
        int X;
        cin >> X;
        for (auto coin : {500, 100, 50, 10, 5, 1}) {
            while(X >= coin) {
                if(!wallet[coin]) {
                    break;
                }
                --wallet[coin];
                X -= coin;
            }
        }
        if(X) {
            is_possible = false;
        }
    }
    cout << (is_possible ? YES : NO) << "\n";
    return 0;
}

#include <algorithm>
#include <cassert>
#include <iostream>
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

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N;
    int K;
    cin >> N >> K;
    int soln = 0;
    int empty = K;
    for (int i = 0; i < N; i++)
    {
        int A;
        cin >> A;
        if (A <= empty)
        {
            empty -= A;
        }
        else
        {
            soln++;
            empty = K - A;
        }
    }
    cout << soln + 1 << "\n";
    return 0;
}

#include <algorithm>
#include <cassert>
#include <iostream>
#include <numeric>
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

#define MOD int(1e8)

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
    cin >> N;
    vi A(N);
    cin >> A;
    sort(all(A));
    lli trouble_pairs = 0;
    for (int i = 0; i < N; i++)
    {
        int idx = lower_bound(A.begin() + i + 1, A.end(), MOD - A[i]) - A.begin();
        trouble_pairs += (N - idx);
    }
    lli total_sum = accumulate(all(A), 0ll);
    cout << ((N - 1) * total_sum) - (trouble_pairs * (lli)(MOD)) << "\n";
    return 0;
}

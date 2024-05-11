#include <algorithm>
#include <bitset>
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

#define MAX_N 2000
#define MAX_A 999

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
    short N, M;
    cin >> N >> M;
    vvs A(N, vs(M));
    cin >> A;
    vector<bitset<MAX_N>> similarity_matrix(N);
    vector<bitset<MAX_N>> rows_having(MAX_A + 1);
    for (int j = 0; j < M; j++)
    {
        for (int i = 0; i < N; i++)
        {
            rows_having[A[i][j]].set(i);
        }
        for (int i = 0; i < N; i++)
        {
            similarity_matrix[i] ^= rows_having[A[i][j]];
        }
        for (int i = 0; i < N; i++)
        {
            rows_having[A[i][j]].reset(i);
        }
    }
    int soln = 0;
    if (M & 1)
    {
        soln -= N;
    }
    for (int i = 0; i < N; i++)
    {
        soln += similarity_matrix[i].count();
    }
    soln = soln / 2;
    cout << soln << "\n";
    return 0;
}

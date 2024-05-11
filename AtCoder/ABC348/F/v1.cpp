#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>

#define YES "Yes"
#define NO "No"

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

bool is_similar(const vector<short> &X, const vector<short> &Y)
{
    short cnt = 0;
    for (short i = 0; i < X.size(); i++)
    {
        if (X[i] == Y[i])
        {
            cnt++;
        }
    }
    return cnt % 2;
}

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    short N, M;
    cin >> N >> M;
    vector<vector<short>> A(N, vector<short>(M));
    cin >> A;
    int soln = 0;
    for (short i = 0; i < N; i++)
    {
        for (short j = i + 1; j < N; j++)
        {
            if (is_similar(A[i], A[j]))
            {
                soln++;
            }
        }
    }
    cout << soln << "\n";
    return 0;
}

#include <algorithm>
#include <cassert>
#include <iostream>
#include <numeric>
#include <vector>

#define YES "Yes"
#define NO "No"

#define all(vec) vec.begin(), vec.end()

using namespace std;

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
    vector<int> A(N - 1);
    cin >> A;
    long long sum = accumulate(all(A), 0ll);
    cout << -sum << "\n";
    return 0;
}
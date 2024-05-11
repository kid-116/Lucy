#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
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
    map<int, int> least_delicious;
    while (N--)
    {
        int A;
        int C;
        cin >> A >> C;
        if (!least_delicious.count(C))
        {
            least_delicious[C] = INT32_MAX;
        }
        least_delicious[C] = min(least_delicious[C], A);
    }
    int best_deliciousness = INT32_MIN;
    for (auto const &[C, A] : least_delicious)
    {
        if (A > best_deliciousness)
        {
            best_deliciousness = A;
        }
    }
    cout << best_deliciousness << "\n";
    return 0;
}
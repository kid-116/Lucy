#include <iostream>
#include <set>
#include <vector>

#define YES "Yes"
#define NO "No"

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
    int N;
    int K;
    cin >> N >> K;
    vector<int> P(N);
    cin >> P;
    vector<int> pos(N, -1);
    for (int i = 0; i < N; i++)
    {
        pos[P[i] - 1] = i;
    }
    int soln = INT32_MAX;
    set<int> interval;
    for (int i = 0; i < N; i++)
    {
        if (interval.size() == K)
        {
            interval.erase(interval.find(pos[i - K]));
        }
        interval.insert(pos[i]);
        if (interval.size() == K)
        {
            soln = min(soln, *interval.rbegin() - *interval.begin());
        }
    }
    cout << soln << "\n";
    return 0;
}

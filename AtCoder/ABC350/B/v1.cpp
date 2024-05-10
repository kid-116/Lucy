#include <algorithm>
#include <cassert>
#include <iostream>
#include <set>
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
    int Q;
    cin >> N >> Q;
    set<int> empty_holes;
    while (Q--)
    {
        int T;
        cin >> T;
        if (empty_holes.find(T) != empty_holes.end())
        {
            empty_holes.erase(empty_holes.find(T));
        }
        else
        {
            empty_holes.insert(T);
        }
    }
    cout << N - empty_holes.size() << "\n";
    return 0;
}

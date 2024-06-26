#include <algorithm>
#include <cassert>
#include <iostream>
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
    long long N;
    int A;
    int X; // N / A
    int Y; // N / b where b is obtained by rolling a die.
    return 0;
}

#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>

#define FAIL 'x'
#define SUCCESS 'o'

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
    for (int i = 1; i <= N; i++)
    {
        cout << ((i % 3 == 0) ? FAIL : SUCCESS);
    }
    cout << "\n";
    return 0;
}
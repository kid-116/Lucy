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
    vector<int> A(N);
    cin >> A;
    map<int, int> pos;
    for (int i = 0; i < A.size(); i++)
    {
        pos[A[i]] = i;
    }
    vector<pair<int, int>> moves;
    for (int i = 0; i < A.size(); i++) {
        int truth = i + 1;
        if(A[i] == truth) {
            continue;
        }
        int j = pos[truth];
        assert(i != j);
        swap(A[i], A[j]);
        pos[A[i]] = i;
        pos[A[j]] = j;
        moves.push_back({i, j});
    }
    assert(moves.size() < N);
    cout << moves.size() << "\n";
    for (const auto &[i, j] : moves)
    {
        cout << i + 1 << " " << j + 1 << "\n";
    }
    return 0;
}

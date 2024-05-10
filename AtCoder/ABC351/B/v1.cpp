#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
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

template <typename T>
class UnionFind
{
    map<T, T> parent;
    map<T, int> size;
    int num_sets;

public:
    UnionFind()
    {
        num_sets = 0;
    }

    void make_set(T v)
    {
        if (parent.count(v))
        {
            throw invalid_argument("Duplicate element.");
        }
        parent[v] = v;
        size[v] = 1;
        ++num_sets;
    }

    int find_set(T v)
    {
        if (parent[v] == v)
        {
            return v;
        }
        parent[v] = find_set(parent[v]);
        return parent[v];
    }

    bool union_sets(T u, T v)
    {
        u = find_set(u);
        v = find_set(v);
        if (u == v)
        {
            return false;
        }
        if (size[u] > size[v])
        {
            swap(u, v);
        }
        parent[v] = u;
        size[u] += size[v];
        --num_sets;
        return true;
    }

    int count()
    {
        return num_sets;
    }
};

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N;
    cin >> N;
    vector<string> A(N);
    vector<string> B(N);
    cin >> A;
    cin >> B;
    for(int i = 0; i < N; i++) {
        for(int j = 0; j < N; j++) {
            if(A[i][j] != B[i][j]) {
                cout << i + 1 << " " << j + 1 << "\n";
                return 0;
            }
        }
    }
    return 0;
}

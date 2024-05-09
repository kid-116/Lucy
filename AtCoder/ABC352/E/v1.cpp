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
    int M;
    cin >> N >> M;
    vector<pair<int, vector<int>>> cliques;
    while (M--)
    {
        int K;
        int C;
        cin >> K >> C;
        vector<int> A(K);
        cin >> A;
        cliques.push_back({C, A});
    }
    sort(all(cliques));
    long long soln = 0;
    UnionFind<int> mst;
    for (int i = 1; i <= N; i++)
    {
        mst.make_set(i);
    }
    for (auto const &[C, A] : cliques)
    {
        for (int i = 1; i < A.size(); i++)
        {
            if (mst.union_sets(A[0], A[i]))
            {
                soln += C;
            }
        }
    }
    if (mst.count() == 1)
    {
        cout << soln;
    }
    else
    {
        cout << -1;
    }
    cout << "\n";
    return 0;
}

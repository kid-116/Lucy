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

    vector<T> sets()
    {
        vector<T> sets;
        for (auto const &[v, par] : parent)
        {
            if (par == v)
            {
                sets.push_back(v);
            }
        }
        return sets;
    }

    int get_size(T v)
    {
        v = find_set(v);
        return size[v];
    }
};

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N;
    int M;
    cin >> N >> M;
    UnionFind<int> sns;
    for (int i = 1; i <= N; i++)
    {
        sns.make_set(i);
    }
    for (int _ = 0; _ < M; _++)
    {
        int A, B;
        cin >> A >> B;
        sns.union_sets(A, B);
    }
    long long soln = 0;
    for (int group : sns.sets())
    {
        int size = sns.get_size(group);
        soln += ((long long)(size) * (size - 1)) / 2;
    }
    soln -= M;
    cout << soln << "\n";
    return 0;
}

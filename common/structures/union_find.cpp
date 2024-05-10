#include <map>

using namespace std;

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

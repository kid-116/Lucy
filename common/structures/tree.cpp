#include <vector>

using namespace std;

template <typename T>
struct Tree
{
    vector<vector<int>> neighbors;
    vector<T> data;
    vector<int> depth;
    vector<long long> subtree_data;
    int root;

    void calc_depths(int node = -1, int par = -1, int d = 0)
    {
        if (node == -1)
        {
            depth.resize(size(), -1);
            return calc_depths(root);
        }
        depth[node] = d;
        for (int neighbor : neighbors[node])
        {
            if (neighbor != par)
            {
                calc_depths(neighbor, node, d + 1);
            }
        }
    }

    int size()
    {
        return neighbors.size();
    }

    long long calc_subtree_data(int node = -1, int par = -1)
    {
        if (node == -1)
        {
            subtree_data.resize(size());
            return calc_subtree_data(root);
        }
        subtree_data[node] = data[node];
        for (int neighbor : neighbors[node])
        {
            if (neighbor != par)
            {
                subtree_data[node] += calc_subtree_data(neighbor, node);
            }
        }
        return subtree_data[node];
    }

    Tree(int n, vector<pair<int, int>> edges, vector<T> data = {}, int root = 0)
    {
        this->root = root;
        neighbors.resize(n);
        this->data = data;
        for (auto &[u, v] : edges)
        {
            --u;
            --v;
            neighbors[u].push_back(v);
            neighbors[v].push_back(u);
        }
        // Pre-processing.
        calc_depths();
        calc_subtree_data();
    }

    long long dfs(int node = -1, int par = -1)
    {
        if (node == -1)
        {
            return dfs(root);
        }
        for (int neighbor : neighbors[node])
        {
            if (neighbor != par)
            {
            }
        }
        return soln;
    }
};

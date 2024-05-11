#include <algorithm>
#include <cassert>
#include <iostream>
#include <numeric>
#include <vector>

#define YES "Yes"
#define NO "No"

#define all(vec) vec.begin(), vec.end()

using namespace std;

template <typename T, typename U>
istream &operator>>(istream &is, pair<T, U> &p)
{
    is >> p.first >> p.second;
    return is;
}
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

    long long dfs(long long soln, const long long data_sum, int node = -1, int par = -1)
    {
        if (node == -1)
        {
            return dfs(soln, data_sum, root);
        }
        for (int neighbor : neighbors[node])
        {
            if (neighbor != par)
            {
                soln = min(soln, dfs(soln - 2 * subtree_data[neighbor] + data_sum,
                                     data_sum,
                                     neighbor,
                                     node));
            }
        }
        return soln;
    }
};

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N;
    cin >> N;
    vector<pair<int, int>> edges(N - 1);
    cin >> edges;
    vector<int> C(N);
    cin >> C;
    Tree<int> town(N, edges, C);
    long long soln = 0;
    for (int i = 0; i < town.size(); i++)
    {
        soln += (long long)(town.depth[i]) * town.data[i];
    }
    cout << town.dfs(soln, accumulate(all(town.data), 0ll)) << "\n";
    return 0;
}

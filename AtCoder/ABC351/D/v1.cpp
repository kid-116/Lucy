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

class Solver
{
    static vector<pair<int, int>> moves;

    vector<string> S;
    int H, W;

    bool is_valid(int i, int j)
    {
        return i >= 0 && i < H && j >= 0 && j < W;
    }

    bool is_magnet(int i, int j)
    {
        return is_valid(i, j) && S[i][j] == '#';
    }

    bool is_end(int i, int j)
    {
        bool is_end = false;
        for (auto const &[dx, dy] : Solver::moves)
        {
            is_end = is_end || is_magnet(i + dx, j + dy);
        }
        return is_end;
    }

    int traverse(int i, int j, vector<vector<bool>> &vis, set<pair<int, int>> &vis_end)
    {
        if (!is_valid(i, j))
        {
            return 0;
        }
        if (is_magnet(i, j))
        {
            return 0;
        }
        if (vis[i][j])
        {
            return 0;
        }
        if (is_end(i, j))
        {
            if(vis_end.find({i, j}) != vis_end.end()) {
                return 0;
            }
            vis_end.insert({i, j});
            return 1;
        }
        int cells_visited = 1;
        vis[i][j] = true;
        for (auto const &[dx, dy] : Solver::moves)
        {
            cells_visited += traverse(i + dx, j + dy, vis, vis_end);
        }
        return cells_visited;
    }

public:
    Solver(vector<string> S)
    {
        Solver::S = S;
        H = S.size();
        W = S.front().length();
    }

    int solve()
    {
        int soln = 1;
        vector<vector<bool>> vis(H, vector<bool>(W, false));
        for (int i = 0; i < H; i++)
        {
            for (int j = 0; j < W; j++)
            {
                if (vis[i][j] || is_end(i, j) || is_magnet(i, j))
                {
                    continue;
                }
                set<pair<int, int>> vis_end;
                soln = max(soln, traverse(i, j, vis, vis_end));
            }
        }
        return soln;
    }
};
vector<pair<int, int>> Solver::moves = {
    {0, -1},
    {0, 1},
    {-1, 0},
    {1, 0}};

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int H, W;
    cin >> H >> W;
    vector<string> S(H);
    cin >> S;
    Solver solver(S);
    cout << solver.solve() << "\n";
    return 0;
}

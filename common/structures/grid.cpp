#include <map>
#include <queue>
#include <vector>

using namespace std;

enum Cell
{
    Start,
    End,
    Blocked,
    Empty,
};

template <typename T, typename U = int>
struct Grid
{
    const static vector<pair<int, int>> moves;

    vector<vector<T>> S;
    vector<vector<U>> data;
    map<Cell, T> legend;
    int H, W;

    bool is_valid(int i, int j)
    {
        return i >= 0 && i < H && j >= 0 && j < W;
    }

    vector<pair<int, int>> neighbours(int i, int j)
    {
        vector<pair<int, int>> neighbours;
        for (const auto &[di, dj] : Grid::moves)
        {
            int ni = i + di, nj = j + dj;
            if (is_valid(ni, nj) && S[ni][nj] != legend[Blocked])
            {
                neighbours.push_back({ni, nj});
            }
        }
        return neighbours;
    }

    bool dfs(int i, int j, vector<vector<bool>> &vis)
    {
        vis[i][j] = true;
        if (S[i][j] == legend[End])
        {
            return true;
        }
        for (auto const &[ni, nj] : neighbours(i, j))
        {
            if (vis[ni][nj])
            {
                continue;
            }
            dfs(ni, nj, vis) ? return true : continue;
        }
        return false;
    }
    bool bfs(const int i, const int j)
    {
        queue<tuple<int, int>> q;
        vector<vector<bool>> vis = init_vis();
        vis[i][j] = true;
        q.push({i, j});
        while (!q.empty())
        {
            auto [i, j] = q.front();
            q.pop();
            if (S[i][j] == legend[End])
            {
                return true;
            }
            for (auto const &[ni, nj] : neighbours(i, j))
            {
                if (vis[ni][nj])
                {
                    continue;
                }
                vis[ni][nj] = true;
                q.push({ni, nj});
            }
        }
        return false;
    }

    pair<int, int> find(Cell cell)
    {
        for (int i = 0; i < H; i++)
        {
            for (int j = 0; j < W; j++)
            {
                if (S[i][j] == legend[cell])
                {
                    return {i, j};
                }
            }
        }
        return {-1, -1};
    }

    vector<vector<bool>> init_vis()
    {
        return vector<vector<bool>>(H, vector<bool>(W, false));
    }

    Grid(vector<vector<T>> S, map<Cell, T> legend, vector<vector<U>> data = {})
    {
        Grid::S = S;
        Grid::data = data;
        Grid::legend = legend;
        H = S.size();
        W = S[0].size();
    }
};
template <typename T, typename U>
const vector<pair<int, int>> Grid<T, U>::moves = {
    {0, -1},
    {0, 1},
    {-1, 0},
    {1, 0}};

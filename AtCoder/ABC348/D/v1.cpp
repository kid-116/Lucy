#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <queue>
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

enum Cell
{
    Start,
    End,
    Blocked,
    Empty,
};

template <typename T, typename U = int>
class Grid
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

    // bool traverse_dfs(int i, int j, vector<vector<bool>> &vis, int energy = 0)
    // {
    //     vis[i][j] = true;
    //     if (data[i][j])
    //     {
    //         energy = data[i][j];
    //         data[i][j] = 0;
    //         vector<vector<bool>> new_vis = init_vis();
    //         return traverse_dfs(i, j, new_vis, energy);
    //     }
    //     if (!energy)
    //     {
    //         return false;
    //     }
    //     if (S[i][j] == legend[End])
    //     {
    //         return true;
    //     }
    //     bool reached_end = false;
    //     for (auto const &[ni, nj] : neighbours(i, j))
    //     {
    //         if (vis[ni][nj])
    //         {
    //             continue;
    //         }
    //         reached_end = reached_end || traverse_dfs(ni, nj, vis, energy - 1);
    //     }
    //     return reached_end;
    // }
    bool bfs(const int i, const int j, const int energy = 0)
    {
        queue<tuple<int, int, int>> q;
        vector<vector<bool>> vis = init_vis();
        vis[i][j] = true;
        q.push({i, j, energy});
        bool can_reach = false;
        while (!q.empty())
        {
            auto [i, j, e] = q.front();
            q.pop();
            if (S[i][j] == legend[End])
            {
                return true;
            }
            if (data[i][j])
            {
                int tmp = data[i][j];
                data[i][j] = 0;
                can_reach = can_reach || bfs(i, j, tmp);
            }
            if (e == 0)
            {
                continue;
            }
            for (auto const &[ni, nj] : neighbours(i, j))
            {
                if (vis[ni][nj])
                {
                    continue;
                }
                vis[ni][nj] = true;
                q.push({ni, nj, e - 1});
            }
        }
        return can_reach;
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

public:
    Grid(vector<vector<T>> S, map<Cell, T> legend, vector<vector<U>> data = {})
    {
        Grid::S = S;
        Grid::data = data;
        Grid::legend = legend;
        H = S.size();
        W = S[0].size();
    }

    bool can_reach()
    {
        auto [si, sj] = find(Start);
        return bfs(si, sj);
    }
};
template <typename T, typename U>
const vector<pair<int, int>> Grid<T, U>::moves = {
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
    vector<vector<char>> A(H, vector<char>(W));
    cin >> A;
    int N;
    cin >> N;
    vector<vector<int>> E(H, vector<int>(W, 0));
    while (N--)
    {
        int r, c;
        int e;
        cin >> r >> c >> e;
        --r;
        --c;
        E[r][c] = e;
    }
    map<Cell, char> legend = {
        {Start, 'S'},
        {End, 'T'},
        {Blocked, '#'},
        {Empty, '.'},
    };
    Grid<char> grid(A, legend, E);
    cout << (grid.can_reach() ? YES : NO) << "\n";
    return 0;
}

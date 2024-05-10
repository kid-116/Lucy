#include <vector>

using namespace std;

template <typename T>
class Grid
{
    const static vector<pair<int, int>> moves;

    vector<vector<T>> S;
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
            if (is_valid(ni, nj))
            {
                neighbours.push_back({ni, nj});
            }
        }
        return neighbours;
    }

    int traverse(int i, int j, vector<vector<bool>> &vis)
    {
        return 0;
    }

public:
    Grid()
    {
        cin >> H >> W;
        S.resize(H, vector<T>(W));
        cin >> S;
    }
};
template <typename T>
const vector<pair<int, int>> Grid<T>::moves = {
    {0, -1},
    {0, 1},
    {-1, 0},
    {1, 0}};

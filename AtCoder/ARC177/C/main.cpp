#include <algorithm>
#include <bitset>
#include <cassert>
#include <cmath>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <vector>

using namespace std;

#define YES "Yes"
#define NO "No"

#define lli long long

#define v16 vector<short>
#define vv16 vector<vs>
#define vb vector<bool>
#define vvb vector<vb>
#define v32 vector<int>
#define vv32 vector<vi>
#define v64 vector<lli>
#define vv64 vector<vl>
#define vc vector<char>
#define vvc vector<vc>
#define vs vector<string>

#define all(vec) vec.begin(), vec.end()

#define MOD 998244353

template <typename T, typename U>
istream &operator>>(istream &is, pair<T, U> &p) {
  is >> p.first >> p.second;
  return is;
}
template <typename T>
istream &operator>>(istream &is, vector<T> &vec) {
  for (T &ele : vec) {
    is >> ele;
  }
  return is;
}

template <typename T>
ostream &operator<<(ostream &os, const vector<T> &vec) {
  for (auto const &ele : vec) {
    os << ele << " ";
  }
  return os;
}
template <typename T, typename U>
ostream &operator<<(ostream &os, const pair<T, U> &p) {
  os << p.second << "(" << p.first << ")" << " ";
  return os;
}

struct Graph {
  int n;
  vector<vector<pair<int, int>>> adj;

  Graph(int n, const vector<tuple<int, int, int>> &edges,
        bool directed = false) {
    Graph::n = n;
    adj.resize(n);
    for (auto [u, v, w] : edges) {
      adj[u].push_back({v, w});
      if (!directed) {
        adj[v].push_back({u, w});
      }
    }
  }

  v64 run_djikstra(int s) {
    v64 d(n, INT64_MAX);
    set<pair<int, int>> q;

    d[s] = 0;
    q.insert({0, s});

    while (!q.empty()) {
      auto [_, u] = *q.begin();
      q.erase(q.begin());
      for (auto const &[to, len] : adj[u]) {
        if (d[u] + len < d[to]) {
          q.erase({d[to], to});
          d[to] = d[u] + len;
          q.insert({d[to], to});
        }
      }
    }

    return d;
  }
};

enum Cell {
  Start,
  End,
  Blocked,
  Empty,
};
template <typename T, typename U = int>
struct Grid {
  const static vector<pair<int, int>> moves;

  vector<vector<T>> S;
  vector<vector<U>> data;
  map<Cell, T> legend;
  int H, W;

  bool is_valid(int i, int j) { return i >= 0 && i < H && j >= 0 && j < W; }

  int get_id(int i, int j) {
    if (!is_valid(i, j)) {
      return -1;
    }
    return i * W + j;
  }

  vector<pair<int, int>> neighbours(int i, int j) {
    vector<pair<int, int>> neighbours;
    for (const auto &[di, dj] : Grid::moves) {
      int ni = i + di, nj = j + dj;
      if (is_valid(ni, nj) && S[ni][nj] != legend[Blocked]) {
        neighbours.push_back({ni, nj});
      }
    }
    return neighbours;
  }

  bool dfs(int i, int j, vector<vector<bool>> &vis) {
    vis[i][j] = true;
    if (S[i][j] == legend[End]) {
      return true;
    }
    for (auto const &[ni, nj] : neighbours(i, j)) {
      if (vis[ni][nj]) {
        continue;
      }
      if (dfs(ni, nj, vis)) {
        return true;
      }
    }
    return false;
  }
  bool bfs(const int i, const int j) {
    queue<tuple<int, int>> q;
    vector<vector<bool>> vis = init_vis();
    vis[i][j] = true;
    q.push({i, j});
    while (!q.empty()) {
      auto [i, j] = q.front();
      q.pop();
      if (S[i][j] == legend[End]) {
        return true;
      }
      for (auto const &[ni, nj] : neighbours(i, j)) {
        if (vis[ni][nj]) {
          continue;
        }
        vis[ni][nj] = true;
        q.push({ni, nj});
      }
    }
    return false;
  }

  pair<int, int> find(Cell cell) {
    for (int i = 0; i < H; i++) {
      for (int j = 0; j < W; j++) {
        if (S[i][j] == legend[cell]) {
          return {i, j};
        }
      }
    }
    return {-1, -1};
  }

  vector<vector<bool>> init_vis() {
    return vector<vector<bool>>(H, vector<bool>(W, false));
  }

  Grid(vector<vector<T>> S, map<Cell, T> legend, vector<vector<U>> data = {}) {
    Grid::S = S;
    Grid::data = data;
    Grid::legend = legend;
    H = S.size();
    W = S[0].size();
  }
};
template <typename T, typename U>
const vector<pair<int, int>> Grid<T, U>::moves = {
    {0, -1}, {0, 1}, {-1, 0}, {1, 0}};

short solve(const vs &c, const char color, int start, int end) {
  map<Cell, char> legend = {
      {Blocked, 'P'},
  };
  const short N = c.size();
  vvc cc(N, vc(N));
  for(short i = 0; i < N; i++) {
    for(short j = 0; j < N; j++) {
      cc[i][j] = c[i][j];
    }
  }
  Grid<char> grid(cc, legend);
  vector<tuple<int, int, int>> edges;
  for (short i = 0; i < N; i++) {
    for (short j = 0; j < N; j++) {
      for (auto const &[ni, nj] : grid.neighbours(i, j)) {
        edges.push_back({grid.get_id(i, j), grid.get_id(ni, nj),
                         grid.S[ni][nj] == color ? 0 : 1});
      }
    }
  }
  Graph graph(N * N, edges, true);
  v64 dist = graph.run_djikstra(start);
  return dist[end];
}

int main() {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  short N;
  cin >> N;
  vector<string> c(N);
  cin >> c;
  short soln = 0;
  soln += solve(c, 'R', 0, N * N - 1);
  soln += solve(c, 'B', N - 1, (N - 1) * N);
  cout << soln << "\n";
  return 0;
}

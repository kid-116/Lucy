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

template <typename T = int>
struct SegmentTree {
  vector<T> length;
  vector<T> lazy;
  int n;

  SegmentTree(int n) {
    this->n = n;
    length.resize(4 * n, 0);
    lazy.resize(4 * n, 0);
  }

  int left_child(int i) { return 2 * i; }

  int right_child(int i) { return 2 * i + 1; }

  void update(int l, int r, T val, int v = 1, int nl = 0, int nr = -1) {
    if (nr == -1) {
      return update(l, r, val, v, nl, n - 1);
    }
    if (l > r) {
      return;
    }
    if (l == nl && r == nr) {
      lazy[v] += val;
    } else {
      int mi = (nl + nr) / 2;
      update(l, min(r, mi), val, left_child(v), nl, mi);
      update(max(l, mi + 1), r, val, right_child(v), mi + 1, nr);
    }
    if (lazy[v]) {
      length[v] = nr + 1 - nl;
    } else if (nr == nl) {
      length[v] = 0;
    } else {
      length[v] = length[left_child(v)] + length[right_child(v)];
    }
  }
};

int main() {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  int N;
  cin >> N;
  v32 A(N);
  cin >> A;
  map<int, v32> pos;
  vector<tuple<int, int, int, int>> rectangles;
  set<tuple<int, int, int, bool>> events;
  for (int i = 0; i < N; i++) {
    pos[A[i]].push_back(i);
  }
  for(int i = 0; i < N; i++) {
    auto it = lower_bound(all(pos[A[i]]), i);
    int l = it == pos[A[i]].begin() ? 0 : *(it - 1) + 1;
    int r = it == pos[A[i]].end() - 1 ? N - 1 : *(it + 1) - 1;
    rectangles.push_back({l, i, i + 1, r + 1});
    int height = r + 1 - i;
    events.insert({l, i, height, true});
    events.insert({i + 1, r + 1, height, false});
  }
  SegmentTree<> tree(N);
  lli soln = 0;
  int prev = get<0>(*events.begin());
  for(auto &[x, y, height, is_start] : events) {
    soln += (lli)(tree.length[1]) * (x - prev);
    if(is_start) {
      tree.update(y, y + height - 1, 1);
    }
    else {
      tree.update(y - height, y - 1, -1);
    }
    prev = x;
  }
  cout << soln << "\n";
  return 0;
}

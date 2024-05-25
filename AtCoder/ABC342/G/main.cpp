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
  vector<T> maxs;
  vector<T> ops;
  int n;

  SegmentTree(int n) {
    this->n = n;
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
  int Q;
  cin >> Q;
  SegmentTree<set<int>> 
  while (Q--) {
    int type;
    cin >> type;
    if(type == 1) {
      continue;
    }
    if(type == 2) {
      continue;
    }
    if(type == 3) {
      continue;
    }
  }
  return 0;
}

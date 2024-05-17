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

struct Solver {
  lli N;
  string S;
  string T;
  map<char, vector<int>> pos;

  Solver(lli N, string S, string T) {
    Solver::N = N;
    Solver::S = S;
    Solver::T = T;

    for (int i = 0; i < S.length(); i++) {
      pos[S[i]].push_back(i);
    }
  }

  bool is_possible(lli k) {
    lli n = N - 1;
    int idx = 0;
    for (char ch : T) {
      if(idx == S.length()) {
        idx = 0;
        --n;
      }
      int in_one = pos[ch].size();
      if (in_one == 0) {
        return false;
      }
      auto it = lower_bound(all(pos[ch]), idx);
      int start = pos[ch].end() - it;
      if(start >= k) {
        idx = *(it + k - 1) + 1;
        continue;
      }
      lli mid = 0;
      int last = 0;
      if(k > start) {
        mid = (k - start) / in_one;
        last = (k - start) % in_one;
      }
      // Start.
      --n;
      idx = 0;
      // Mid.
      n -= mid;
      if(last == 0) {
        ++n;
        idx = pos[ch].back() + 1;
      }
      else {
        idx = pos[ch][last - 1] + 1;
      }
    }
    return n >= 0;
  }

  lli solve() {
    lli lo = 0, hi = (lli)(N) * S.length() / T.length();
    lli soln = 0;
    while (lo <= hi) {
      lli mi = (lo + hi + 1) / 2;
      if (is_possible(mi)) {
        lo = mi + 1;
        soln = max(soln, mi);
      } else {
        hi = mi - 1;
      }
    }
    return soln;
  }
};

int main() {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  lli N;
  string S;
  string T;
  cin >> N;
  cin >> S;
  cin >> T;
  Solver solver(N, S, T);
  lli soln = solver.solve();
  cout << soln << "\n";
  return 0;
}

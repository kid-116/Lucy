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

int main() {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  int N;
  cin >> N;
  string S;
  cin >> S;
  v32 C(N);
  cin >> C;
  v64 suf_a(N + 1, 0), suf_b(N + 1, 0);
  for (int i = N - 1; i >= 0; i--) {
    suf_a[i] = suf_a[i + 1];
    suf_b[i] = suf_b[i + 1];
    if (i % 2 == 0) {
      if (S[i] == '0') {
        suf_a[i] += C[i];
      } else {
        suf_b[i] += C[i];
      }
    } else {
      if (S[i] == '0') {
        suf_b[i] += C[i];
      } else {
        suf_a[i] += C[i];
      }
    }
  }
  lli soln = INT64_MAX;
  for (int i = 0; i < S.length() - 1; i++) {
    if (i % 2 == 0) {
      // ... 0 0 ...
      soln = min(soln, suf_b[0] - suf_b[i + 1] + suf_a[i + 1]);
      // ... 1 1 ...
      soln = min(soln, suf_a[0] - suf_a[i + 1] + suf_b[i + 1]);
    } else {
      // ... 0 0 ...
      soln = min(soln, suf_a[0] - suf_a[i + 1] + suf_b[i + 1]);
      // ... 1 1 ...
      soln =  min(soln, suf_b[0] - suf_b[i + 1] + suf_a[i + 1]);
    }
  }
  cout << soln << "\n";
  return 0;
}

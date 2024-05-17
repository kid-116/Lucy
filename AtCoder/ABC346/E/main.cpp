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
  int H, W;
  int M;
  cin >> H >> W >> M;
  v16 T(M);  // Row/1, Col/2
  v32 A(M);  // Index.
  v32 X(M);  // Color.
  for (int i = 0; i < M; i++) {
    cin >> T[i] >> A[i] >> X[i];
  }
  map<int, lli> freq;
  set<int> col_cols, col_rows;
  lli tot = 0;
  for (int i = M - 1; i >= 0; i--) {
    tot -= freq[X[i]];
    if (T[i] == 1) {
      if (col_rows.find(A[i]) == col_rows.end()) {
        freq[X[i]] += W - col_cols.size();
        col_rows.insert(A[i]);
      }
    } else {
      if (col_cols.find(A[i]) == col_cols.end()) {
        freq[X[i]] += H - col_rows.size();
        col_cols.insert(A[i]);
      }
    }
    tot += freq[X[i]];
    if (freq[X[i]] == 0) {
      freq.erase(X[i]);
    }
  }
  lli zero_colored = (lli)(H)*W - tot;
  if (zero_colored) {
    freq[0] += zero_colored;
  }
  cout << freq.size() << "\n";
  for (auto const &[c, f] : freq) {
    cout << c << " " << f << "\n";
  }
  return 0;
}

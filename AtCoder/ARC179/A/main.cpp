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
  int K;
  cin >> N >> K;
  v32 A(N);
  cin >> A;
  sort(all(A));
  if (K > 0) {
    cout << YES << "\n";
    cout << A << "\n";
  }
  else {
    if (accumulate(all(A), 0ll) < K) {
      cout << NO << "\n";
    }
    else {
      cout << YES << "\n";
      reverse(all(A));
      cout << A << "\n";
    }
  }
  return 0;
}

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

typedef long long lli;

typedef vector<short> v16;
typedef vector<v16> vv16;
typedef vector<bool> vb;
typedef vector<vb> vvb;
typedef vector<int> v32;
typedef vector<v32> vv32;
typedef vector<lli> v64;
typedef vector<v64> vv64;
typedef vector<char> vc;
typedef vector<vc> vvc;
typedef vector<string> vs;

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
  int M;
  cin >> N >> M;
  v32 A(M);
  cin >> A;
  sort(all(A));
  if(A.front() == 1 || A.back() == N) {
    cout << -1 << "\n";
    return 0;
  }
  v32 soln(N, -1);
  iota(all(soln), 1);
  soln.erase(soln.begin() + A.front() - 1);
  soln.insert(soln.begin() + A.back(), A.front());
  cout << soln << "\n";
  return 0;
}

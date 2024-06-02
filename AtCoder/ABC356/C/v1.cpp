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

#define MAX_N 15

typedef bitset<MAX_N> KeyGroup;
typedef pair<KeyGroup, bool> Test;

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

int solve(int idx, const int N, const int K, KeyGroup &is_real, const vector<Test> &test) {
    if (idx >= N) {
        bool possible = true;
        for (auto &[key_grp, success] : test) {
            int num_real_keys = (key_grp & is_real).count();
            if (num_real_keys >= K != success) {
                possible = false;
            }
        }
        return (possible ? 1 : 0);
    }
    int soln = 0;
    is_real.set(idx);
    soln += solve(idx + 1, N, K, is_real, test);
    is_real.reset(idx);
    soln += solve(idx + 1, N, K, is_real, test);
    return soln;
}

int main() {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  int N; // Number of keys.
  int M; // Number of tests.
  int K; // Threshold for opening the door.
  cin >> N >> M >> K;
  vector<Test> test(M);
  for (int t = 0; t < M; t++) {
    int C;
    cin >> C;
    while(C--) {
        int A;
        cin >> A;
        --A;
        test[t].first.set(A);
    }
    char R;
    cin >> R;
    test[t].second = (R == 'o');
  }
  KeyGroup is_real;
  int soln = solve(0, N, K, is_real, test);
  cout << soln << "\n";
  return 0;
}

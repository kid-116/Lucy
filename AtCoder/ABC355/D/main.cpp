#include <algorithm>
#include <iostream>
#include <vector>

typedef long long lli;

using namespace std;

int main() {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  int N;
  cin >> N;
  vector<pair<int, int>> ends;
  for (int i = 0; i < N; i++) {
    int l, r;
    cin >> l >> r;
    ends.push_back({l, 0});
    ends.push_back({r, 1});
  }
  sort(ends.begin(), ends.end());
  lli pairs = 0;
  int n_active = 0;
  for (auto &[pt, is_end] : ends) {
    if (is_end == 0) {
      pairs += n_active;
      ++n_active;
    } else {
      --n_active;
    }
  }
  cout << pairs << "\n";
  return 0;
}

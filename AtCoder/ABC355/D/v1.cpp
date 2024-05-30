#include <iostream>
#include <set>

typedef long long lli;

using namespace std;

int main() {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  int N;
  cin >> N;
  set<pair<int, bool>> ends;
  for (int i = 0; i < N; i++) {
    int l, r;
    cin >> l >> r;
    ends.insert({l, false});
    ends.insert({r, true});
  }
  lli pairs = 0;
  // int n_active = 0;
  // for (auto &[pt, is_end] : ends) {
  //   if (!is_end) {
  //     pairs += n_active;
  //     ++n_active;
  //   } else {
  //     --n_active;
  //   }
  // }
  cout << pairs << "\n";
  return 0;
}

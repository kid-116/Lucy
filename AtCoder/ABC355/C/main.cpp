#include <iostream>
#include <vector>

using namespace std;

int main() {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  int N;
  int T;
  cin >> N >> T;
  vector<int> row_cnt(N, 0), col_cnt(N, 0);
  int tl = 0, tr = 0;
  int ans = -1;
  for (int t = 1; t <= T; t++) {
    int A;
    cin >> A;
    int i = (A - 1) / N;
    int j = (A - 1) % N;
    bool bingo = false;
    ++row_cnt[i];
    ++col_cnt[j];
    if (i == j) {
      ++tl;
    }
    if (i + j == N - 1) {
      ++tr;
    }
    if (row_cnt[i] == N) {
      bingo = true;
    }
    if (col_cnt[j] == N) {
      bingo = true;
    }
    // if (N % 2) {
    if (tl == N) {
      bingo = true;
    }
    if (tr == N) {
      bingo = true;
    }
    // }
    if (bingo && ans == -1) {
      ans = t;
    }
  }
  cout << ans << "\n";
  return 0;
}

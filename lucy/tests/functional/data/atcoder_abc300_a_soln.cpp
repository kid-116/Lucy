#include <iostream>

using namespace std;

int main() {
  int N;
  int A, B;
  cin >> N >> A >> B;
  for (int i = 1; i <= N; i++) {
    int C;
    cin >> C;
    if (A + B == C) {
      cout << i << "\n";
    }
  }
  return 0;
}

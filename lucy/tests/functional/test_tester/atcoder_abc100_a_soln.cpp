#include <iostream>

using namespace std;

int main() {
  int A, B;
  cin >> A >> B;
  cout << ((A <= 8 && B <= 8) ? "Yay!" : ":(") << "\n";
  return 0;
}

map<int, int> factorize(int n) {
  map<int, int> power;
  while (n % 2 == 0) {
    n /= 2;
    ++power[2];
  }
  for (int i = 3; i <= sqrt(n); i += 2) {
    while (n % i == 0) {
      n /= i;
      ++power[i];
    }
  }
  return power;
}

bool is_prime(int n) {
  assert(n >= 1);
  if (n == 1) {
    return false;
  }
  if (n == 2) {
    return true;
  }
  map<int, int> factors = factorize(n);
  return factors.size() == 0;
}

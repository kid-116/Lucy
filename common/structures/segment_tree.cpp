template <typename T = int>
struct SegmentTree {
  vector<T> length;
  vector<T> lazy;
  int n;

  SegmentTree(int n) {
    this->n = n;
    length.resize(4 * n, 0);
    lazy.resize(4 * n, 0);
  }

  int left_child(int i) { return 2 * i; }

  int right_child(int i) { return 2 * i + 1; }

  void update(int l, int r, T val, int v = 1, int nl = 0, int nr = -1) {
    if (nr == -1) {
      return update(l, r, val, v, nl, n - 1);
    }
    if (l > r) {
      return;
    }
    if (l == nl && r == nr) {
      lazy[v] += val;
    } else {
      int mi = (nl + nr) / 2;
      update(l, min(r, mi), val, left_child(v), nl, mi);
      update(max(l, mi + 1), r, val, right_child(v), mi + 1, nr);
    }
    if (lazy[v]) {
      length[v] = nr + 1 - nl;
    } else if (nr == nl) {
      length[v] = 0;
    } else {
      length[v] = length[left_child(v)] + length[right_child(v)];
    }
  }
};

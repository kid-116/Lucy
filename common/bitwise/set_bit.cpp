int leftmost_set_bit(int n) {
    int pos = -1;
    while(n) {
        n >>= 1;
        pos++;
    }
    return pos;
}
int leftmost_but_set_bit(int n) {
    int leftmost = leftmost_set_bit(n);
    return leftmost_set_bit(n ^ (1 << leftmost));
}
int rightmost_set_bit(int n) {
    return leftmost_set_bit(n & -n);
}

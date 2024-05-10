#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>

#define YES "Yes"
#define NO "No"

#define all(vec) vec.begin(), vec.end()

using namespace std;

template <typename T>
istream &operator>>(istream &is, vector<T> &vec)
{
    for (T &ele : vec)
    {
        is >> ele;
    }
    return is;
}

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

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    long long L, R;
    cin >> L >> R;
    vector<pair<long long, long long>> intervals_back;
    while(R > L) {
        long long left = R - (R & -R);
        if(left < L) {
            break;
        }
        intervals_back.push_back({left, R});
        R = left;
    }
    reverse(all(intervals_back));
    vector<pair<long long, long long>> intervals_front;
    while(L != R) {
        long long right = L + (L & -L);
        intervals_front.push_back({L, right});
        L = right;
    }
    vector<pair<long long, long long>> intervals;
    intervals.insert(intervals.end(), all(intervals_front));
    intervals.insert(intervals.end(), all(intervals_back));
    cout << intervals.size() << "\n";
    for (auto const &[l, r] : intervals)
    {
        cout << l << " " << r << "\n";
    }
    return 0;
}

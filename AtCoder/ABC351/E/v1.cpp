#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
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

template <typename T>
struct Point
{
    T x, y;

    Point(T x, T y) : x(x), y(y) {}

    friend std::istream &operator>>(std::istream &is, Point &p)
    {
        is >> p.x >> p.y;
        return is;
    }

    void rotate_shift()
    {
        int x_shifted = x + y;
        int y_shifted = x - y;
        x = x_shifted;
        y = y_shifted;
    }
};

template <typename T>
long long sum_abs_diff_all_pairs(vector<T> &vec)
{
    sort(all(vec));
    long long tot_sum = accumulate(all(vec), 0ll);
    long long running = 0;
    long long soln = 0;
    for (int i = 0; i < vec.size(); i++)
    {
        T &ele = vec[i];
        soln += (long long)(ele)*i - running;
        soln += (tot_sum - running - ele) - (long long)(ele) * (vec.size() - i - 1);
        running += ele;
    }
    return soln / 2;
}

template <typename T>
long long sum_dist_all_pairs(vector<Point<T>> &points)
{
    long long soln = 0;
    vector<T> x, y;
    for (Point<T> &p : points)
    {
        x.push_back(p.x);
        y.push_back(p.y);
    }
    soln += sum_abs_diff_all_pairs(x);
    soln += sum_abs_diff_all_pairs(y);
    return soln;
}

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N;
    cin >> N;
    vector<Point<int>> Pa, Pb;
    for (int i = 0; i < N; i++)
    {
        int X, Y;
        cin >> X >> Y;
        Point<int> p(X, Y);
        p.rotate_shift();
        if ((X - Y) % 2)
        {
            Pa.push_back(p);
        }
        else
        {
            Pb.push_back(p);
        }
    }
    long long soln = 0;
    soln += sum_dist_all_pairs(Pa);
    soln += sum_dist_all_pairs(Pb);
    cout << soln / 2 << "\n";
    return 0;
}

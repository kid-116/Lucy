#include <algorithm>
#include <cassert>
#include <cmath>
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

template <typename T>
class Point
{
    T x, y;

public:
    Point(T x = 0, T y = 0)
    {
        this->x = x;
        this->y = y;
    }

    friend std::istream &operator>>(std::istream &is, Point &p)
    {
        is >> p.x >> p.y;
        return is;
    }

    long long dist_sq(Point &other)
    {
        return pow(x - other.x, 2) + pow(y - other.y, 2);
    }
};

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N;
    cin >> N;
    vector<Point<int>> points(N);
    cin >> points;
    for (int i = 0; i < N; i++)
    {
        int farthest = i;
        for (int j = 0; j < N; j++)
        {
            if (i == j)
            {
                continue;
            }
            if (points[i].dist_sq(points[farthest]) < points[i].dist_sq(points[j]))
            {
                farthest = j;
            }
        }
        cout << farthest + 1 << "\n";
    }
    return 0;
}

template <typename T>
class Point
{
    T x, y;

public:
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

#include <set>

using namespace std;

auto cmp = [](pair<int, int> a, pair<int, int> b)
{
    int len_a = a.second - a.first;
    int len_b = b.second - b.first;
    if (len_a < len_b)
    {
        return true;
    }
    else if (len_a == len_b)
    {
        // return false;
        return a < b;
    }
    else
    {
        return false;
    }
};
multiset<pair<int, int>, decltype(cmp)> groups(cmp);

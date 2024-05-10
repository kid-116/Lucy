#include <algorithm>
#include <cassert>
#include <cmath>
#include <ctype.h>
#include <iostream>
#include <map>
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

char toggle_case(char ch)
{
    if (isalpha(ch))
    {
        if (islower(ch))
        {
            return toupper(ch);
        }
        else
        {
            return tolower(ch);
        }
    }
    return ch;
}

class Solver
{
    string S;
    map<int, int> left, right;

public:
    Solver(string str)
    {
        S = str;
        vector<int> par_stack;
        for (int i = 0; i < S.length(); i++)
        {
            char &ch = S[i];
            if (isalpha(ch))
            {
                if (par_stack.size() % 2)
                {
                    ch = toggle_case(ch);
                }
            }
            else if (ch == '(')
            {
                par_stack.push_back(i);
            }
            else if (ch == ')')
            {
                right[par_stack.back()] = i;
                left[i] = par_stack.back();
                par_stack.pop_back();
            }
        }
    }

    void solve(int l = 0, int r = -1, int depth = 0)
    {
        if (r == -1)
        {
            r = S.length();
        }
        if (depth % 2)
        {
            for(int i = r - 1; i >= l; i--) {
                if (S[i] == ')')
                {
                    solve(left[i] + 1, i, depth + 1);
                    i = left[i];
                    continue;
                }
                else {
                    cout << S[i];
                }
            }
        }
        else
        {
            for (int i = l; i < r; i++)
            {
                if (S[i] == '(')
                {
                    solve(i + 1, right[i], depth + 1);
                    i = right[i];
                    continue;
                }
                else {
                    cout << S[i];
                }
            }
        }
    }
};

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    string S = "((XYZ)n(X(y)Z))";
    cin >> S;
    Solver solver(S);
    solver.solve();
    cout << "\n";
    return 0;
}

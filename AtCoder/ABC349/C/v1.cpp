#include <algorithm>
#include <cassert>
#include <iostream>
#include <cstring>
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

void toupper(string &S)
{
    for (char &ch : S)
    {
        ch = toupper(ch);
    }
}
void tolower(string &S)
{
    for (char &ch : S)
    {
        ch = tolower(ch);
    }
}

bool is_subseq(const string &sub, const string &str)
{
    int i = 0;
    for (char ch : str)
    {
        if (ch == sub[i])
        {
            i++;
        }
        if (i == sub.size())
        {
            return true;
        }
    }
    return false;
}

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    string S = "narita";
    string T = "NRX";
    cin >> S;
    cin >> T;
    if (T.back() == 'X')
    {
        T = T.substr(0, T.size() - 1);
    }
    tolower(T);
    cout << (is_subseq(T, S) ? YES : NO) << "\n";
    return 0;
}

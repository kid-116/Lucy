#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
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

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    string S;
    cin >> S;
    map<char, int> freq;
    for (char ch : S)
    {
        if (!freq.count(ch))
        {
            freq[ch] = 0;
        }
        freq[ch]++;
    }
    map<int, int> freq_freq;
    for (auto [_, f] : freq)
    {
        if (!freq_freq.count(f))
        {
            freq_freq[f] = 0;
        }
        freq_freq[f]++;
    }
    for (auto [_, f] : freq_freq)
    {
        if (f != 2)
        {
            cout << NO << "\n";
            return 0;
        }
    }
    cout << YES << "\n";
    return 0;
}

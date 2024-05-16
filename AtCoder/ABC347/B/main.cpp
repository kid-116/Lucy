#include <algorithm>
#include <bitset>   //
#include <cassert>  //
#include <cmath>    //
#include <iostream> //
#include <map>      //
#include <numeric>  //
#include <set>      //
#include <vector>   //

using namespace std; //

#define YES "Yes"
#define NO "No"

#define lli long long

#define vs vector<short>
#define vvs vector<vs>
#define vb vector<bool>
#define vvb vector<vb>
#define vi vector<int>
#define vvi vector<vi>
#define vl vector<lli>
#define vvl vector<vvl>

#define all(vec) vec.begin(), vec.end()

#define MOD 998244353

template <typename T, typename U>
istream &operator>>(istream &is, pair<T, U> &p)
{
    is >> p.first >> p.second;
    return is;
}
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
ostream &operator<<(ostream &os, const vector<T> &vec)
{
    for (auto const &ele : vec)
    {
        os << ele << " ";
    }
    return os;
}
template <typename T, typename U>
ostream &operator<<(ostream &os, const pair<T, U> &p)
{
    os << p.second << "(" << p.first << ")" << " ";
    return os;
}

struct TrieNode
{
    map<char, TrieNode *> children = {};
    int num_str = 0;
    int is_end = 0;
};
template <typename T = int>
struct Trie
{
    TrieNode *root;

    Trie()
    {
        root = new TrieNode();
    }

    int count(const string &str)
    {
        TrieNode *node = root;
        for (char ch : str)
        {
            if (!node->children.count(ch))
            {
                return 0;
            }
            node = node->children[ch];
        }
        return node->is_end;
    }

    void insert(const string &str, bool exists_ok = true)
    {
        if (!exists_ok)
        {
            if (count(str))
            {
                return;
            }
        }
        TrieNode *node = root;
        for (char ch : str)
        {
            ++node->num_str;
            if (!node->children.count(ch))
            {
                node->children[ch] = new TrieNode();
            }
            node = node->children[ch];
        }
        ++node->num_str;
        ++node->is_end;
    }
};

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    string S;
    cin >> S;
    Trie<int> trie;
    for (int i = 0; i < S.length(); i++)
    {
        for (int j = i + 1; j <= S.length(); j++)
        {
            trie.insert(S.substr(i, j - i), false);
        }
    }
    cout << trie.root->num_str << "\n";
    return 0;
}

#include <algorithm>
#include <bitset>
#include <cassert>
#include <cmath>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <vector>

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

using namespace std;

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
struct TrieNode
{
    map<char, TrieNode *> children = {};
    T agg = 0;
    int is_end = 0;
};
template <typename T = int>
struct Trie
{
    TrieNode<T> *root;

    Trie()
    {
        root = new TrieNode<T>();
    }

    void insert(const string &str)
    {
        TrieNode<T> *node = root;
        for (char ch : str)
        {
            ++node->agg;
            if (!node->children.count(ch))
            {
                node->children[ch] = new TrieNode<T>();
            }
            node = node->children[ch];
        }
        ++node->agg;
        ++node->is_end;
    }
};

void dfs(TrieNode<int> *node, lli &soln, int depth = 0)
{
    vector<int> aggs;
    for (auto [ch, child] : node->children)
    {
        aggs.push_back(child->agg);
        dfs(child, soln, depth + 1);
    }
    lli total_sum = accumulate(all(aggs), 0ll);
    lli sum_squares = 0;
    for (int agg : aggs)
    {
        sum_squares += (lli)(agg) * agg;
    }
    lli is_end = node->is_end;
    soln += (total_sum * total_sum -
             sum_squares +
             (2 * total_sum * is_end) +
             is_end * (is_end - 1)) *
            depth;
}

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N;
    cin >> N;
    Trie trie;
    while (N--)
    {
        string S;
        cin >> S;
        trie.insert(S);
    }
    lli soln = 0;
    dfs(trie.root, soln);
    soln = soln / 2;
    cout << soln << endl;
    return 0;
}

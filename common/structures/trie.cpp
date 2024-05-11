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

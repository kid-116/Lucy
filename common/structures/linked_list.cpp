template <typename T>
struct Node
{
    T data;
    Node<T> *next;
    Node<T> *prev;

    Node(T data, Node *prev = nullptr, Node *next = nullptr)
    {
        Node::data = data;
        Node::prev = prev;
        Node::next = next;
    }
};

template <typename T>
struct LinkedList
{
    Node<T> *head = nullptr;
    vector<Node<T> *> index;
    bool is_indexed = false;
    int length = 0;

    LinkedList(vector<T> &vec, bool is_indexed = false)
    {
        LinkedList::is_indexed = is_indexed;
        length = vec.size();
        if (is_indexed)
        {
            index.resize(vec.size(), nullptr);
        }
        Node<T> *prev = nullptr;
        int idx = 0;
        for (auto &ele : vec)
        {
            Node<T> *node = new Node(ele, prev);
            if (is_indexed)
            {
                index[idx] = node;
            }
            index[idx] = node;
            if (!head)
            {
                head = node;
            }
            if (prev)
            {
                prev->next = node;
            }
            prev = node;
            ++idx;
        }
    }

    bool is_valid_index(int i)
    {
        return i >= 0 && i < length;
    }

    vector<Node<T> *> traverse()
    {
        vector<Node<T> *> nodes;
        Node<T> *ptr = head;
        while (ptr)
        {
            nodes.push_back(ptr);
            ptr = ptr->next;
        }
        return nodes;
    }

    friend std::ostream &operator<<(std::ostream &os, LinkedList<T> &list)
    {
        for (auto &node : list.traverse())
        {
            cout << node->data << " ";
        }
        return os;
    }
};

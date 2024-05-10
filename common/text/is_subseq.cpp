#include <string>

using namespace std;

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

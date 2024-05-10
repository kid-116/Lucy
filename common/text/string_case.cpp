#include <string>

using namespace std;

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

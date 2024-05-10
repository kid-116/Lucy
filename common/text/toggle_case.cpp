#include <ctype.h>

using namespace std;

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

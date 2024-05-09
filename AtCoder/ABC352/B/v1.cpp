#include <iostream>

#define YES "Yes"
#define NO "No"

using namespace std;

int main()
{
    string S;
    string T;
    cin >> S;
    cin >> T;
    int Si, Ti;
    Si = Ti = 0;
    while (Si < S.length())
    {
        if (T[Ti] == S[Si])
        {
            cout << Ti + 1 << " ";
            ++Si;
        }
        ++Ti;
    }
    cout << "\n";
    return 0;
}

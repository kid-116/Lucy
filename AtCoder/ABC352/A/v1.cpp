#include <iostream>

#define YES "Yes"
#define NO "No"

using namespace std;

int main()
{
    int N;
    int X, Y;
    int Z;
    cin >> N >> X >> Y >> Z;
    if (Y < X)
    {
        swap(X, Y);
    }
    if (Z >= X && Z <= Y)
    {
        cout << YES;
    }
    else
    {
        cout << NO;
    }
    cout << "\n";
    return 0;
}

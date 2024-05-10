#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>

#define YES "Yes"
#define NO "No"

using namespace std;

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    string S;
    cin >> S;
    S = S.substr(3);
    int contest_id = stoi(S);
    if (contest_id == 316 || contest_id >= 350 || contest_id <= 0)
    {
        cout << NO;
    }
    else
    {
        cout << YES;
    }
    cout << "\n";
    return 0;
}

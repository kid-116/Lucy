#include <iostream>

#define YES "Yes"
#define NO "No"

using namespace std;

int main()
{
    int N;
    cin >> N;
    long long soln = 0;
    int tallest_head = 0;
    while (N--)
    {
        int A, B;
        cin >> A >> B;
        soln += A;
        tallest_head = max(tallest_head, B - A);
    }
    soln += tallest_head;
    cout << soln << "\n";
}

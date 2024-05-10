from functools import cache

N, A, X, Y = map(int, input().split())


@cache
def f(n):
    if n == 0:
        return 0
    opt_a = X + f(n // A)
    opt_b = 6 / 5 * Y + 1 / 5 * sum(f(n // b) for b in range(2, 7))
    return min(opt_a, opt_b)


print(f(N))

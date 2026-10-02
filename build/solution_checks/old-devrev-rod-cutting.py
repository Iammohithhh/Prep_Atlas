def solution(n, v):
    dp = [0] * (n + 1)
    for length in range(1, n + 1):
        best = 0
        for cut in range(1, length + 1):
            best = max(best, v[cut] + dp[length - cut])
        dp[length] = best
    return dp[n]

# ---- tests
import random
assert solution(4, [0, 2, 4, 7, 7]) == 9
for _ in range(200):
    n = random.randint(1, 8); v = [0] + [random.randint(0, 9) for _ in range(n)]
    def go(l): return 0 if l == 0 else max(v[i] + go(l - i) for i in range(1, l + 1))
    assert solution(n, v) == go(n)
print('ok')

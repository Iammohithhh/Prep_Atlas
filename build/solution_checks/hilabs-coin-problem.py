import random
from itertools import combinations
MOD = 10**9 + 7

def solve(n, k, m):
    # coins have amounts 0..n-1; count k-subsets whose sum is divisible by m
    dp = [[0] * m for _ in range(k + 1)]
    dp[0][0] = 1
    for c in range(n):
        r = c % m
        for j in range(min(k, c + 1), 0, -1):
            prev, cur = dp[j - 1], dp[j]
            for s in range(m):
                v = prev[s]
                if v:
                    t = (s + r) % m
                    cur[t] = (cur[t] + v) % MOD
    return dp[k][0]

def brute(n, k, m):
    return sum(1 for c in combinations(range(n), k) if sum(c) % m == 0) % MOD

assert solve(4, 2, 2) == 2
for _ in range(300):
    n = random.randint(1, 10)
    k = random.randint(1, n)
    m = random.randint(1, 7)
    assert solve(n, k, m) == brute(n, k, m)
print('ok')

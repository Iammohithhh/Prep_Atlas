MOD = 10**9 + 7
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def count_subsets(n, a):
    cnt = {}
    for v in a:
        cnt[v] = cnt.get(v, 0) + 1
    dp = [0] * 1024                               # dp[mask] = ways to pick a subset whose product has exactly these primes
    dp[0] = 1
    for v, c in cnt.items():
        mask = 0
        ok = True
        for i, p in enumerate(PRIMES):
            if v % p == 0:
                if v % (p * p) == 0:
                    ok = False                     # not square-free
                    break
                mask |= 1 << i
        if not ok or mask == 0:
            continue
        for s in range(1023, -1, -1):              # descending so each value is used at most once
            if s & mask == 0 and dp[s]:
                dp[s | mask] = (dp[s | mask] + dp[s] * c) % MOD
    return (sum(dp) - 1) % MOD                      # drop the empty subset

# ---- tests
import random
from itertools import combinations
assert count_subsets(3, [2, 6, 12]) == 2
assert count_subsets(4, [4, 5, 6, 15]) == 4
def squarefree_gt1(x):
    if x < 2: return False
    d = 2
    while d * d <= x:
        if x % (d * d) == 0: return False
        d += 1
    return True
def brute(a):
    n = len(a); tot = 0
    for r in range(1, n + 1):
        for idx in combinations(range(n), r):
            prod = 1
            for i in idx: prod *= a[i]
            if squarefree_gt1(prod): tot += 1
    return tot
for _ in range(300):
    a = [random.randint(2, 30) for _ in range(random.randint(1, 10))]
    assert count_subsets(len(a), a) == brute(a), a
count_subsets(10000, [random.randint(2, 30) for _ in range(10000)])
print('ok')

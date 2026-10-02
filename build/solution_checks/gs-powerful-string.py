MOD = 10**9 + 7


def count_ways(s):
    n = len(s)
    p = 1
    while p < n and s[p] == s[0]:
        p += 1                                       # length of the leading run
    if p == n:                                       # all characters equal: any substring may be removed
        return n * (n + 1) // 2 % MOD
    q = 1
    while s[n - 1 - q] == s[n - 1]:
        q += 1                                       # length of the trailing run
    if s[0] == s[-1]:
        return (p + 1) * (q + 1) % MOD
    return (p + q + 1) % MOD

# ---- tests
import random
def brute(s):
    n = len(s); c = 0
    for l in range(n):
        for r in range(l, n):
            rest = s[:l] + s[r + 1:]
            if len(set(rest)) <= 1: c += 1
    return c % MOD
assert count_ways("aaa") == 6
for _ in range(500):
    s = ''.join(random.choice('ab') for _ in range(random.randint(1, 12)))
    assert count_ways(s) == brute(s), s
print('ok')

import random
from functools import lru_cache

def maximumTower(N, K, f):
    NEG = float('-inf')
    vals = sorted(set(f))
    # dp[c][v]: max towers received so far with c changes used and current frequency vals[v]
    dp = [[0] * len(vals) for _ in range(K + 1)]     # initial frequency is free
    for x in f:
        nd = [[NEG] * len(vals) for _ in range(K + 1)]
        for c in range(K + 1):
            for vi, v in enumerate(vals):
                cur = dp[c][vi]
                if cur == NEG:
                    continue
                if v != x:                                  # tower does not receive, signal unchanged
                    nd[c][vi] = max(nd[c][vi], cur)
                else:                                       # receives; may keep or change the frequency
                    nd[c][vi] = max(nd[c][vi], cur + 1)
                    if c < K:
                        for wi in range(len(vals)):
                            if wi != vi:
                                nd[c + 1][wi] = max(nd[c + 1][wi], cur + 1)
        dp = nd
    return max(max(row) for row in dp)

def brute(N, K, f):
    vals = sorted(set(f))
    best = 0
    @lru_cache(None)
    def rec(i, freq, k):
        if i == N:
            return 0
        if f[i] != freq:
            return rec(i + 1, freq, k)
        res = 1 + rec(i + 1, freq, k)
        if k < K:
            for w in vals:
                if w != freq:
                    res = max(res, 1 + rec(i + 1, w, k + 1))
        return res
    return max(rec(0, v, 0) for v in vals)

assert maximumTower(5, 1, [10, 10, 30, 40, 30]) == 4
for _ in range(300):
    n = random.randint(1, 8)
    K = random.randint(1, 3)
    f = [random.randint(1, 4) for _ in range(n)]
    assert maximumTower(n, K, f) == brute(n, K, tuple(f)), (n, K, f)
print('ok')

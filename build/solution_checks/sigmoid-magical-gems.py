import random
from itertools import product

def magicalGems(input1, input2):
    a = sorted(input2, reverse=True)          # groups are contiguous in sorted-desc order
    n = len(a)
    pre = [0]
    for v in a: pre.append(pre[-1] + v)
    NEG = float('-inf')
    dp = [NEG] * (n + 1); dp[0] = 0
    for i in range(1, n + 1):
        for j in range(i):
            dp[i] = max(dp[i], dp[j] + (i - j) * (pre[i] - pre[j]))
    return dp[n]

def brute(a):
    n = len(a); best = None
    # assign each element a group label (restricted growth strings)
    def rec(i, labels, k):
        nonlocal best
        if i == n:
            tot = 0
            for g in range(k):
                grp = [a[t] for t in range(n) if labels[t] == g]
                tot += len(grp) * sum(grp)
            best = tot if best is None else max(best, tot)
            return
        for g in range(k + 1):
            rec(i + 1, labels + [g], max(k, g + 1))
    rec(0, [], 0)
    return best

assert magicalGems(4, [2, -7, 9, 9]) == 53
assert magicalGems(2, [2, 2]) == 8
for _ in range(300):
    n = random.randint(1, 7)
    a = [random.randint(-9, 9) for _ in range(n)]
    assert magicalGems(n, a) == brute(a), a
print('ok')

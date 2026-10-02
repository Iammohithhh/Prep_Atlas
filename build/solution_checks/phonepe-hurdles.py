import random
from collections import deque
from itertools import combinations

def maxScore(n, k, a):
    INF = float('inf')
    dp = [INF] * (n + 1); dp[0] = 0
    dq = deque([0])                          # window minimum over dp[i-k-1 .. i-1]
    for i in range(1, n + 1):
        while dq and dq[0] < i - k - 1: dq.popleft()
        dp[i] = a[i - 1] + dp[dq[0]]
        while dq and dp[dq[-1]] >= dp[i]: dq.pop()
        dq.append(i)
    best = min(dp[j] for j in range(max(0, n - k), n + 1))
    return sum(a) - best

def brute(n, k, a):
    best = 0
    for mask in range(1 << n):
        run = 0; ok = True; s = 0
        for i in range(n):
            if mask >> i & 1:
                run += 1; s += a[i]
                if run > k: ok = False; break
            else: run = 0
        if ok: best = max(best, s)
    return best

assert maxScore(6, 2, [1, 2, 3, 1, 6, 10]) == 21
assert maxScore(5, 4, [1, 2, 3, 4, 5]) == 14
for _ in range(500):
    n = random.randint(1, 10); k = random.randint(1, n)
    a = [random.randint(0, 9) for _ in range(n)]
    assert maxScore(n, k, a) == brute(n, k, a), (n, k, a)
print('ok')

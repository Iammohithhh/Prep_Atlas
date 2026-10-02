import random
import numpy as np
from math import isqrt

def countSubarrays(n, a):
    M = 1
    while M <= n: M <<= 1
    cnt = np.zeros(M, dtype=np.int64)
    cnt[0] += 1
    p = 0
    for v in a:
        p ^= v; cnt[p] += 1
    idx = np.arange(M)
    bad = int((cnt * (cnt - 1) // 2).sum())          # xor == 0
    s = 1
    while s * s < M:
        sq = s * s
        bad += int((cnt * cnt[idx ^ sq]).sum()) // 2
        s += 1
    return n * (n + 1) // 2 - bad

def brute(n, a):
    c = 0
    for i in range(n):
        x = 0
        for j in range(i, n):
            x ^= a[j]
            if x > 0 and isqrt(x) ** 2 != x: c += 1
    return c

assert countSubarrays(3, [3, 1, 2]) == 4
assert countSubarrays(5, [4, 2, 1, 5, 3]) == 11
for _ in range(300):
    n = random.randint(2, 12)
    a = [random.randint(1, n) for _ in range(n)]
    assert countSubarrays(n, a) == brute(n, a)
print('ok')

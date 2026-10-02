import random
from collections import Counter

def maxBoxes(n, x, a):
    cnt = Counter(v % x for v in a)
    pairs = cnt[0] // 2
    for r in range(1, x // 2 + 1):
        if 2 * r == x:
            pairs += cnt[r] // 2
        else:
            pairs += min(cnt[r], cnt[x - r])
    return 2 * pairs

def brute(a, x):
    n = len(a); best = 0
    def rec(i, used, c):
        nonlocal best
        best = max(best, c)
        for j in range(i, n):
            if j in used: continue
            for k in range(j + 1, n):
                if k in used: continue
                if (a[j] + a[k]) % x == 0:
                    rec(j + 1, used | {j, k}, c + 2)
    rec(0, frozenset(), 0)
    return best

assert maxBoxes(5, 4, [10, 7, 6, 5, 1]) == 4
for _ in range(300):
    n = random.randint(1, 8); x = random.randint(1, 6)
    a = [random.randint(1, 20) for _ in range(n)]
    assert maxBoxes(n, x, a) == brute(a, x), (a, x)
print('ok')

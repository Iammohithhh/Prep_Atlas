import random
from functools import lru_cache

def maxPoints(a):
    a = sorted(a); n = len(a)
    if n == 1: return a[0]
    return sum(a[i] * (i + 2 if i < n - 1 else n) for i in range(n - 1)) + a[-1] * n

def brute(a):
    n = len(a)
    @lru_cache(None)
    def f(mask):
        items = [a[i] for i in range(n) if mask >> i & 1]
        s = sum(items)
        if len(items) == 1: return s
        best = 0
        sub = (mask - 1) & mask
        while sub:
            other = mask ^ sub
            if sub < other or True:
                best = max(best, f(sub) + f(other))
            sub = (sub - 1) & mask
        return s + best
    return f((1 << n) - 1)

assert maxPoints([4, 2, 6]) == 34
assert maxPoints([11]) == 11
for _ in range(200):
    n = random.randint(1, 7)
    a = [random.randint(1, 20) for _ in range(n)]
    assert maxPoints(a) == brute(a), a
print('ok')

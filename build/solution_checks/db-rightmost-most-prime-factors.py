import random
from collections import deque

def omega_sieve(limit):
    om = [0] * (limit + 1)
    for p in range(2, limit + 1):
        if om[p] == 0:                            # p is prime
            for m in range(p, limit + 1, p):
                om[m] += 1
    return om

def solve(x, n, a):
    om = omega_sieve(max(a) if a else 0)
    dq = deque()                                  # indices with strictly decreasing omega
    best = None
    for i in range(n):
        while dq and om[a[dq[-1]]] <= om[a[i]]:   # <= keeps the rightmost among ties
            dq.pop()
        dq.append(i)
        if dq[0] <= i - x:
            dq.popleft()
        if i >= x - 1:
            v = a[dq[0]]
            best = v if best is None else min(best, v)
    return best

def brute(x, n, a):
    om = omega_sieve(max(a))
    res = None
    for i in range(n - x + 1):
        w = a[i:i + x]
        m = max(om[v] for v in w)
        rightmost = [v for v in w if om[v] == m][-1]
        res = rightmost if res is None else min(res, rightmost)
    return res

assert solve(3, 5, [2, 4, 6, 10, 5]) == 6
for _ in range(300):
    n = random.randint(1, 10)
    x = random.randint(1, n)
    a = [random.randint(0, 60) for _ in range(n)]
    assert solve(x, n, a) == brute(x, n, a)
print('ok')

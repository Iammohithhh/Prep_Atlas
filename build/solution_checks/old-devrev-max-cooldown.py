def max_cooldown(n, c, d, arr):
    a = sorted(arr, reverse=True)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]

    def total(k):
        cycle = k + 1
        full, rem = divmod(d, cycle)
        return full * pre[min(n, cycle)] + pre[min(n, rem)]

    if total(0) < c:
        return -1
    if total(d) >= c:                       # k = d already behaves like "never repeat": any larger k works too
        return -1
    lo, hi = 0, d                           # total(lo) >= c, total(hi) < c
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if total(mid) >= c:
            lo = mid
        else:
            hi = mid
    return lo

# ---- tests
import random
assert max_cooldown(2, 5, 4, [1, 2]) == 2
def feasible(arr, d, c, k):
    n = len(arr)
    best = {}
    from functools import lru_cache
    @lru_cache(None)
    def go(day, last):                       # last = tuple of the day each exercise was last used (-inf if never)
        if day > d: return 0
        res = go(day + 1, last)               # idle
        for i in range(n):
            if day - last[i] > k:
                nl = list(last); nl[i] = day
                res = max(res, arr[i] + go(day + 1, tuple(nl)))
        return res
    return go(1, tuple([-10**9] * n)) >= c
def brute(n, c, d, arr):
    ks = [k for k in range(0, d + 2) if feasible(arr, d, c, k)]
    if not ks or 0 not in ks: return -1
    if max(ks) >= d + 1: return -1
    return max(ks)
for _ in range(150):
    n = random.randint(2, 3); d = random.randint(1, 6); arr = [random.randint(1, 4) for _ in range(n)]
    c = random.randint(1, 15)
    assert max_cooldown(n, c, d, arr) == brute(n, c, d, arr), (n, c, d, arr)
print('ok')

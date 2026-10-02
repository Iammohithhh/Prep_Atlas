def get_min_diff(cost, m):
    n = len(cost)
    if n == 1:
        return 0
    a = sorted(cost)
    total = sum(a)
    pre = [0]
    for v in a:
        pre.append(pre[-1] + v)
    from bisect import bisect_left, bisect_right

    def raise_cost(L):                       # unit increases to lift every value below L up to L
        k = bisect_left(a, L)
        return L * k - pre[k]

    def lower_cost(U):                       # unit decreases to bring every value above U down to U
        k = bisect_right(a, U)
        return (pre[n] - pre[k]) - U * (n - k)

    lo, hi = a[0], a[-1]
    while lo < hi:                           # highest L with raise_cost(L) <= m
        mid = (lo + hi + 1) // 2
        if raise_cost(mid) <= m:
            lo = mid
        else:
            hi = mid - 1
    L = lo
    lo, hi = a[0], a[-1]
    while lo < hi:                           # lowest U with lower_cost(U) <= m
        mid = (lo + hi) // 2
        if lower_cost(mid) <= m:
            hi = mid
        else:
            lo = mid + 1
    U = lo
    if L >= U:
        return 0 if total % n == 0 else 1
    return U - L

# ---- tests
import random
assert get_min_diff([1, 1, 4, 2], 1) == 2
def brute(cost, m):
    a = sorted(cost)
    for _ in range(m):
        if a[0] == a[-1]:
            break
        a[-1] -= 1
        a[0] += 1
        a.sort()
    return a[-1] - a[0]
for _ in range(600):
    n = random.randint(1, 6)
    c = [random.randint(1, 12) for _ in range(n)]
    m = random.randint(1, 30)
    assert get_min_diff(c, m) == brute(c, m), (c, m)
print('ok')

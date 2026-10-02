def max_or_array(a):
    n = len(a)
    total = 0
    for x in a:
        total |= x
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] | a[i]
    suf = [0] * (n + 2)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] | a[i]
    best = 0
    r = 0
    for l in range(n + 1):
        if r < l:
            r = l
        while r < n and (pre[l] | suf[r + 1]) == total:   # try to remove a[l..r]
            r += 1
        # removed block is a[l..r-1]
        if (pre[l] | suf[r]) == total:
            best = max(best, r - l)
    return best

# ---- tests
import random
assert max_or_array([1, 4, 24, 2]) == 0
assert max_or_array([2, 1, 1, 5, 4, 4, 8, 1]) == 4
def brute(a):
    n = len(a); total = 0
    for x in a: total |= x
    best = 0
    for l in range(n):
        for r in range(l, n + 1):
            rest = 0
            for i in range(n):
                if not (l <= i < r): rest |= a[i]
            if rest == total: best = max(best, r - l)
    return best
for _ in range(500):
    a = [random.randint(0, 15) for _ in range(random.randint(1, 9))]
    assert max_or_array(a) == brute(a), a
print('ok')

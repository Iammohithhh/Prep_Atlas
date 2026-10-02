def max_value(k, prices):
    a = sorted(prices)

    def can(d):                                   # can we pick k elements pairwise at least d apart?
        picked = 1
        last = a[0]
        for x in a[1:]:
            if x - last >= d:
                picked += 1
                last = x
                if picked >= k:
                    return True
        return picked >= k

    lo, hi = 0, a[-1] - a[0]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo

# ---- tests
import random
from itertools import combinations
assert max_value(3, [13, 5, 1, 8, 21, 2]) == 8
assert max_value(2, [1, 3, 1]) == 2
assert max_value(2, [7, 7, 7, 7]) == 0
for _ in range(300):
    p = [random.randint(1, 30) for _ in range(random.randint(2, 8))]; k = random.randint(2, len(p))
    best = max(min(b - a for a, b in zip(sorted(c), sorted(c)[1:])) for c in combinations(p, k))
    assert max_value(k, p) == best
print('ok')

def get_maximum_distance(location, k):
    pts = sorted(location)
    n = len(pts)

    def intervals(width):
        count = 0
        i = 0
        while i < n:
            count += 1
            limit = pts[i] + width
            while i < n and pts[i] <= limit:
                i += 1
        return count

    lo, hi = 0, pts[-1] - pts[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if intervals(mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return (lo + 1) // 2                                # integer centre: radius = ceil(width / 2)

# ---- tests
import random
from itertools import combinations
assert get_maximum_distance([1, 9, 3, 10, 14], 2) == 3
assert get_maximum_distance([5, 3, 8], 3) == 0
def brute(loc, k):
    lo, hi = min(loc), max(loc)
    best = 10**9
    for cs in combinations(range(lo, hi + 1), min(k, hi - lo + 1)):
        best = min(best, max(min(abs(x - c) for c in cs) for x in loc))
    return best
for _ in range(300):
    n = random.randint(1, 7); k = random.randint(1, n); loc = [random.randint(1, 16) for _ in range(n)]
    assert get_maximum_distance(loc, k) == brute(loc, k), (loc, k)
print('ok')

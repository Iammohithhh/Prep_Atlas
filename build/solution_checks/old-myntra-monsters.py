from functools import lru_cache
from math import gcd


def destroy_monsters(a):
    @lru_cache(None)
    def go(t):
        k = len(t)
        if k == 0:
            return 0
        pos = sorted({0, k // 2, k - 1})                 # first, second-middle, last (deduplicated)
        best = float('inf')
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                p, q = pos[i], pos[j]
                rest = tuple(t[x] for x in range(k) if x not in (p, q))
                best = min(best, gcd(t[p], t[q]) + go(rest))
        return best
    return go(tuple(a))

# ---- tests
assert destroy_monsters([1, 2, 3, 4]) == 2
assert destroy_monsters([2, 4, 8, 6]) == 4
print('ok')

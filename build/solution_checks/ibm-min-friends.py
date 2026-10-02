def min_friends(num_nodes, num_edges):
    """Smallest possible size of the largest clique (everyone knows everyone) over all graphs with the given counts."""
    n = num_nodes

    def turan(r):                                   # max edges of a graph on n nodes with no clique larger than r
        q, rem = divmod(n, r)
        return (n * n - (r - rem) * q * q - rem * (q + 1) * (q + 1)) // 2

    if num_edges == 0:
        return 1
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if num_edges <= turan(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

# ---- tests
import random
from itertools import combinations
assert min_friends(2, 1) == 1 + 1
assert min_friends(3, 2) == 2
assert min_friends(4, 6) == 4
assert min_friends(5, 7) == 3
def max_clique(n, edges):
    es = set(edges); best = 1 if n else 0
    for r in range(2, n + 1):
        for c in combinations(range(n), r):
            if all(p in es for p in combinations(c, 2)): best = r
    return best
def brute(n, e):
    all_pairs = list(combinations(range(n), 2))
    if e == 0: return 1
    return min(max_clique(n, list(sel)) for sel in combinations(all_pairs, e))
for n in range(2, 7):
    for e in range(0, n * (n - 1) // 2 + 1):
        assert min_friends(n, e) == brute(n, e), (n, e)
print('ok')

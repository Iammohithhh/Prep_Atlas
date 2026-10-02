def longest_chain(tiles):
    rr = tiles.count('RR')
    gg = tiles.count('GG')
    rg = tiles.count('RG')
    gr = tiles.count('GR')
    if rg == 0 and gr == 0:
        return max(rr, gg)
    # both loop colours become reachable; RG and GR alternate
    return rr + gg + 2 * min(rg, gr) + (1 if rg != gr else 0)

# ---- tests
import random
from itertools import permutations
assert longest_chain(["RR", "GR", "RG", "GR", "GR", "RR"]) == 5
assert longest_chain(["GG", "GG", "RR", "GG", "RR"]) == 3
def brute(tiles):
    n = len(tiles); best = 0
    for r in range(1, n + 1):
        for perm in set(permutations(tiles, r)):
            if all(perm[i][1] == perm[i + 1][0] for i in range(r - 1)): best = max(best, r)
    return best
for _ in range(300):
    t = [random.choice(['RR', 'RG', 'GR', 'GG']) for _ in range(random.randint(1, 7))]
    assert longest_chain(t) == brute(t), t
print('ok')

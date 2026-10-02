from collections import Counter


def get_minimum_groups(vulnerability):
    counts = sorted(Counter(vulnerability).values())
    distinct = sorted(set(counts))
    best = None
    # group sizes are s or s+1; try the largest feasible s first (fewer groups)
    for s in range(counts[0], 0, -1):
        total = 0
        ok = True
        for c in counts:
            k = -(-c // (s + 1))                 # fewest groups of size <= s+1
            if k * s > c:                         # even those groups cannot all have size >= s
                ok = False
                break
            total += k
        if ok:
            return total
    return len(vulnerability)

# ---- tests
import random
assert get_minimum_groups([2, 3, 3, 3, 2, 1]) == 4
assert get_minimum_groups([1, 7, 7, 7, 1]) == 2
assert get_minimum_groups([2, 3, 3, 2, 2, 3, 2, 2, 2, 2, 3]) == 3
def brute(vul):
    counts = list(Counter(vul).values())
    best = len(vul)
    for s in range(1, max(counts) + 1):
        total = 0; ok = True
        for c in counts:
            opts = [k for k in range(1, c + 1) if k * s <= c <= k * (s + 1)]
            if not opts: ok = False; break
            total += min(opts)
        if ok: best = min(best, total)
    return best
for _ in range(500):
    vul = [random.randint(1, 4) for _ in range(random.randint(1, 20))]
    assert get_minimum_groups(vul) == brute(vul), vul
print('ok')

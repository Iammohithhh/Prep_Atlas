def longest_subsequence(n, k, queries):
    # build the array as segments with constant values using a difference map over interval endpoints
    diff = {}
    for l, r, x in queries:
        diff[l] = diff.get(l, 0) + x
        diff[r + 1] = diff.get(r + 1, 0) - x
    points = sorted(diff)
    values = []                                     # values of consecutive constant segments, left to right
    cur = 0
    for i, p in enumerate(points):
        cur += diff[p]
        if cur > 0:                                 # zero or negative cells cannot be used (positive integers only)
            values.append(cur)
    # chain DP: best[v] = longest chain Z, Z+K, ..., v ending with value v seen so far in position order
    best = {}
    for v in values:
        cand = best.get(v - k, 0) + 1
        if cand > best.get(v, 0):
            best[v] = cand
    if not best:
        return []
    length = max(best.values())
    z = min(v - (length - 1) * k for v, c in best.items() if c == length)
    return [length] + [z + i * k for i in range(length)]

# ---- tests
import random
assert longest_subsequence(2, 1, [(1, 2, 1), (2, 4, 1)]) == [2, 1, 2]
assert longest_subsequence(4, 2, [(1, 3, 1), (2, 4, 2), (5, 6, 3), (5, 5, 1)]) == [2, 1, 3]
def brute(n, k, queries):
    size = max(r for _, r, _ in queries)
    arr = [0] * (size + 1)
    for l, r, x in queries:
        for i in range(l, r + 1): arr[i] += x
    arr = [v for v in arr[1:] if v > 0]
    bestlen, bestz = 0, None
    # try every Z present in the array as the start and greedily match
    for z in set(arr):
        j = 0; need = z
        for v in arr:
            if v == need:
                j += 1; need += k
        # greedy earliest matching is optimal for a fixed chain
        if j > bestlen or (j == bestlen and (bestz is None or z < bestz)):
            bestlen, bestz = j, z
    return [bestlen] + [bestz + i * k for i in range(bestlen)] if bestlen else []
for _ in range(500):
    n = random.randint(1, 5); k = random.randint(1, 3)
    qs = []
    for _ in range(n):
        l = random.randint(1, 8); r = random.randint(l, 9); qs.append((l, r, random.randint(1, 3)))
    assert longest_subsequence(n, k, qs) == brute(n, k, qs), (n, k, qs)
print('ok')

def find_max_length(skills, k):
    # f[j] = dict value -> best length of a subsequence ending with that value using at most j unequal adjacencies
    f = [dict() for _ in range(k + 1)]
    g = [0] * (k + 1)                              # g[j] = best length over all end values with at most j changes
    for v in skills:
        for j in range(k, -1, -1):                 # descending: g[j-1] is still the value from before this element
            best = max(f[j].get(v, 0) + 1, 1)
            if j >= 1:
                best = max(best, g[j - 1] + 1)
            f[j][v] = best
            if best > g[j]:
                g[j] = best
    return g[k]

# ---- tests
import random
from itertools import combinations
assert find_max_length([1, 1, 2, 3, 2, 1], 2) == 5
assert find_max_length([1, 1, 2, 3], 1) == 3
def brute(s, k):
    n = len(s); best = 0
    for mask in range(1, 1 << n):
        sub = [s[i] for i in range(n) if mask >> i & 1]
        if sum(1 for a, b in zip(sub, sub[1:]) if a != b) <= k: best = max(best, len(sub))
    return best
for _ in range(400):
    n = random.randint(1, 10); s = [random.randint(1, 3) for _ in range(n)]; k = random.randint(1, n)
    assert find_max_length(s, k) == brute(s, k), (s, k)
print('ok')

from collections import defaultdict


def count_stable_segments(capacity):
    """Count pairs l < r with capacity[l] == capacity[r] and sum(capacity[l+1:r]) == capacity[r]."""
    prefix_by_sum = defaultdict(lambda: defaultdict(int))   # prefix sum (inclusive) -> value at that index -> count
    total = 0
    cur = 0
    for i in range(len(capacity) - 1):
        cur += capacity[i]
        r = capacity[i + 1]
        need = cur - r                       # prefix sum up to l must equal cur - capacity[r]
        total += prefix_by_sum[need].get(r, 0)   # ...and capacity[l] must equal capacity[r]
        prefix_by_sum[cur][capacity[i]] += 1
    return total

# ---- tests
import random
def brute(c):
    n = len(c); t = 0
    for l in range(n):
        for r in range(l + 2, n):
            if c[l] == c[r] and sum(c[l + 1:r]) == c[r]: t += 1
    return t
assert count_stable_segments([9, 3, 3, 3, 9]) == 2
for _ in range(500):
    c = [random.randint(1, 5) for _ in range(random.randint(1, 14))]
    assert count_stable_segments(c) == brute(c), c
print('ok')

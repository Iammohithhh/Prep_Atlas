def min_taps(n, ranges):
    reach = [0] * (n + 1)                     # reach[i] = furthest right end of a tap interval starting at or before i
    for i, r in enumerate(ranges):
        lo, hi = max(0, i - r), min(n, i + r)
        reach[lo] = max(reach[lo], hi)
    taps = end = far = i = 0
    while end < n:
        while i <= end:                       # every tap that starts inside the watered prefix
            far = max(far, reach[i])
            i += 1
        if far <= end:
            return -1                         # cannot extend the watered prefix
        taps += 1
        end = far
    return taps

# ---- tests
import random
assert min_taps(5, [3, 4, 1, 1, 0, 0]) == 1
assert min_taps(3, [0, 0, 0, 0]) == -1
assert min_taps(7, [1, 2, 1, 0, 2, 1, 0, 1]) == 3
def brute(n, ranges):
    best = None
    m = len(ranges)
    for mask in range(1 << m):
        iv = sorted((max(0, i - ranges[i]), min(n, i + ranges[i])) for i in range(m) if mask >> i & 1)
        pos = 0
        for lo, hi in iv:
            if lo <= pos:
                pos = max(pos, hi)
        if pos >= n:
            c = bin(mask).count('1')
            if best is None or c < best:
                best = c
    return -1 if best is None else best
for _ in range(500):
    n = random.randint(1, 8)
    ranges = [random.randint(0, 4) for _ in range(n + 1)]
    assert min_taps(n, ranges) == brute(n, ranges), (n, ranges)
print('ok')

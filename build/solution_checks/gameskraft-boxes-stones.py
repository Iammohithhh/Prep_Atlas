def min_boxes_and_time(a, b):
    n = len(a)
    total = sum(a)
    order = sorted(range(n), key=lambda i: -b[i])
    cap = 0
    k = 0
    for i in order:                                  # fewest boxes: take the biggest capacities
        cap += b[i]
        k += 1
        if cap >= total:
            break
    # choose exactly k boxes with total capacity >= total keeping as many stones in place as possible
    NEG = -1
    # dp[j][c] = max sum of A over j chosen boxes with capacity c (c capped at total)
    dp = [[NEG] * (total + 1) for _ in range(k + 1)]
    dp[0][0] = 0
    for i in range(n):
        for j in range(min(k, i + 1), 0, -1):
            row, prev = dp[j], dp[j - 1]
            for c in range(total + 1):
                if prev[c] >= 0:
                    nc = min(total, c + b[i])
                    v = prev[c] + a[i]
                    if v > row[nc]:
                        row[nc] = v
    kept = dp[k][total]
    return k, total - kept

# ---- tests
import random
from itertools import combinations
assert min_boxes_and_time([1, 2, 3], [3, 3, 3]) == (2, 1)
def brute(a, b):
    n = len(a); total = sum(a)
    for k in range(1, n + 1):
        best = None
        for S in combinations(range(n), k):
            if sum(b[i] for i in S) >= total:
                moved = total - sum(a[i] for i in S)
                if best is None or moved < best: best = moved
        if best is not None: return k, best
for _ in range(400):
    n = random.randint(1, 7)
    a = [random.randint(0, 6) for _ in range(n)]
    b = [x + random.randint(0, 6) for x in a]
    if sum(a) == 0: continue
    assert min_boxes_and_time(a, b) == brute(a, b), (a, b)
print('ok')

def min_covers(a, b, c):
    """b is a permutation of 1..a. Covering k books means covering the k thickest."""
    def feasible(k):
        threshold = a - k                          # thickness > threshold is covered
        prefix = [0] * (a + 1)
        for i in range(a):
            prefix[i + 1] = prefix[i] + (1 if b[i] > threshold else -1)
        best_min = float('inf')
        for end in range(c, a + 1):                # window [start, end) with length >= c
            best_min = min(best_min, prefix[end - c])
            if prefix[end] - best_min > 0:
                return True
        return False

    lo, hi = 1, a
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

# ---- tests
import random
assert min_covers(5, [2, 3, 5, 1, 4], 3) == 2
assert min_covers(4, [2, 3, 1, 4], 2) == 2
def brute(a, b, c):
    for k in range(1, a + 1):
        cov = [1 if x > a - k else -1 for x in b]
        for i in range(a):
            for j in range(i + c, a + 1):
                if sum(cov[i:j]) > 0: return k
for _ in range(500):
    a = random.randint(1, 10); b = list(range(1, a + 1)); random.shuffle(b); c = random.randint(1, a)
    assert min_covers(a, b, c) == brute(a, b, c), (a, b, c)
print('ok')

def min_area(x, y, k):
    n = len(x)
    pts = sorted(zip(x, y))
    xs = sorted(set(x))
    best = None
    for i in range(len(xs)):
        for j in range(i, len(xs)):
            lo, hi = xs[i], xs[j]
            ys = sorted(py for px, py in pts if lo <= px <= hi)
            if len(ys) < k:
                continue
            span_x = hi - lo
            for t in range(len(ys) - k + 1):
                side = max(span_x, ys[t + k - 1] - ys[t]) + 2
                if best is None or side * side < best:
                    best = side * side
    return best

# ---- tests
import random
assert min_area([1, 1, 2], [1, 2, 1], 3) == 9
def brute(x, y, k):
    best = None
    for a in range(-2, 9):
        for b in range(-2, 9):
            for s in range(1, 12):
                if sum(1 for px, py in zip(x, y) if a < px < a + s and b < py < b + s) >= k:
                    if best is None or s * s < best:
                        best = s * s
    return best
for _ in range(300):
    n = random.randint(1, 6)
    x = [random.randint(0, 6) for _ in range(n)]
    y = [random.randint(0, 6) for _ in range(n)]
    k = random.randint(1, n)
    assert min_area(x, y, k) == brute(x, y, k), (x, y, k)
print('ok')

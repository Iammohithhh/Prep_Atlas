from itertools import permutations


def recover(values):
    """values = [A, B, C, D], a mix of speed, alpha (d+t), beta (d*t), delta (t-d).
    Returns [distance, time] or [-1, -1]."""
    for speed, alpha, beta, delta in permutations(values):
        if (alpha - delta) % 2 or (alpha + delta) % 2:
            continue
        d = (alpha - delta) // 2       # alpha - delta = 2d
        t = (alpha + delta) // 2       # alpha + delta = 2t
        if t == 0 or abs(d) <= abs(t):
            continue
        if d * t == beta and d // t == speed:
            return [d, t]
    return [-1, -1]

# ---- tests
import random
assert recover([-2, 1, 22, 120]) == [12, 10]
assert recover([1, 2, 3, 4]) == [-1, -1]
for _ in range(300):
    t = random.randint(1, 30); d = random.randint(t + 1, 60)
    vals = [d // t, d + t, d * t, t - d]
    random.shuffle(vals)
    assert recover(vals) == [d, t], (d, t, vals)
print('ok')

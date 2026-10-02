def max_power(x):
    n = len(x)
    base = sum((i + 1) * v for i, v in enumerate(x))
    pre = [0]
    for v in x:
        pre.append(pre[-1] + v)
    best = 0                                           # no move
    for i in range(1, n + 1):
        xi = x[i - 1]
        for j in range(1, n + 1):
            if j > i:                                  # move panel i so that it ends at position j (shifting i+1..j left)
                gain = (j - i) * xi - (pre[j] - pre[i])
            elif j < i:                                # move panel i to position j (shifting j..i-1 right)
                gain = (j - i) * xi + (pre[i - 1] - pre[j - 1])
            else:
                continue
            best = max(best, gain)
    return base + best

# ---- tests
import random
assert max_power([8, 1, 6, 3, 4]) == 78
assert max_power([3, 5, -9, 10]) == 52
def brute(x):
    n = len(x); best = sum((i + 1) * v for i, v in enumerate(x))
    for i in range(n):
        rest = x[:i] + x[i + 1:]
        for j in range(n):
            y = rest[:j] + [x[i]] + rest[j:]
            best = max(best, sum((t + 1) * v for t, v in enumerate(y)))
    return best
for _ in range(400):
    x = [random.randint(-9, 9) for _ in range(random.randint(1, 8))]
    assert max_power(x) == brute(x), x
print('ok')

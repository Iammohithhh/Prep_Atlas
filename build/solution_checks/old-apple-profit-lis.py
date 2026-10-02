from bisect import bisect_left


def longest_profit(data):
    tails = []
    for v in data:
        i = bisect_left(tails, v)
        if i == len(tails):
            tails.append(v)
        else:
            tails[i] = v
    return len(tails)

# ---- tests
import random
from itertools import combinations
assert longest_profit([-1, 9, 0, 8, -5, 6, -24]) == 3
assert longest_profit([]) == 0
assert longest_profit([5, 5, 5]) == 1
def brute(a):
    best = 0
    for mask in range(1 << len(a)):
        s = [a[i] for i in range(len(a)) if mask >> i & 1]
        if all(s[i] < s[i + 1] for i in range(len(s) - 1)):
            best = max(best, len(s))
    return best
for _ in range(300):
    a = [random.randint(-4, 4) for _ in range(random.randint(0, 9))]
    assert longest_profit(a) == brute(a)
print('ok')

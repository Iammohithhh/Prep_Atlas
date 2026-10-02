import random
from collections import Counter
from itertools import product

def maxItems(input1, input2):
    freq = sorted(Counter(input2).values(), reverse=True)
    total, limit = 0, float('inf')
    for f in freq:
        take = min(f, limit - 1)
        if take <= 0: break
        total += take
        limit = take
    return total

def brute(items):
    fr = list(Counter(items).values())
    best = 0
    for choice in product(*[range(f + 1) for f in fr]):
        pos = [c for c in choice if c > 0]
        if len(pos) == len(set(pos)):
            best = max(best, sum(pos))
    return best

assert maxItems(6, [4,1,6,3,6,5]) == 3
assert maxItems(7, [3,7,1,1,3,1,7]) == 6
for _ in range(300):
    n = random.randint(1, 9)
    a = [random.randint(1, 4) for _ in range(n)]
    assert maxItems(n, a) == brute(a), a
print('ok')

def min_wildcards(patterns):
    m = len(patterns[0])
    count = 0
    for col in range(m):
        letters = {p[col] for p in patterns if p[col] != '?'}
        if len(letters) >= 2:
            count += 1
    return count

# ---- tests
import random
from itertools import product
assert min_wildcards(["ha???rrank", "?a?ke?bank"]) == 1
def inter(p, q):
    return all(a == b or a == '?' or b == '?' for a, b in zip(p, q))
def brute(patterns):
    m = len(patterns[0]); alphabet = 'abc?'
    best = m
    for t in product(alphabet, repeat=m):
        if all(inter(t, p) for p in patterns): best = min(best, t.count('?'))
    return best
for _ in range(300):
    m = random.randint(1, 4); k = random.randint(1, 3)
    pats = [''.join(random.choice('ab?') for _ in range(m)) for _ in range(k)]
    assert min_wildcards(pats) == brute(pats), pats
print('ok')

import random
from collections import Counter
from itertools import permutations

def solve(s):
    c = Counter(s)
    half = ''.join(ch * (c[ch] // 2) for ch in sorted(c))
    odd = [ch for ch in sorted(c) if c[ch] % 2]
    mid = odd[0] if odd else ''
    return half + mid + half[::-1]

def brute(s):
    best = ''
    n = len(s)
    for L in range(n, 0, -1):
        cands = set()
        from itertools import combinations
        for idx in combinations(range(n), L):
            sub = ''.join(s[i] for i in idx)
            for p in set(permutations(sub)):
                t = ''.join(p)
                if t == t[::-1]: cands.add(t)
        if cands: return min(cands)

assert solve('adskassda') == 'adsasda'
assert solve('talent') == 'tat'
assert solve('decrypt') == 'c'
for _ in range(100):
    s = ''.join(random.choice('abc') for _ in range(random.randint(1, 6)))
    assert solve(s) == brute(s), s
print('ok')

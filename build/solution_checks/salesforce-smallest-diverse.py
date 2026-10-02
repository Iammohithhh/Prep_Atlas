def smallest_diverse(a, b, c):
    cnt = {'a': a, 'b': b, 'c': c}

    def feasible(rem, last, run):
        """Can the remaining letters be appended after a run of `run` copies of `last`?"""
        total = sum(rem.values())
        if total == 0:
            return True
        for ch, m in rem.items():
            others = total - m
            cap = 2 * (others + 1) - (run if ch == last else 0)
            if m > cap:
                return False
        return True

    out = []
    last, run = '', 0
    for _ in range(a + b + c):
        for ch in 'abc':
            if cnt[ch] == 0:
                continue
            if ch == last and run == 2:
                continue
            cnt[ch] -= 1
            nrun = run + 1 if ch == last else 1
            if feasible(cnt, ch, nrun):
                out.append(ch)
                last, run = ch, nrun
                break
            cnt[ch] += 1
    return ''.join(out)

# ---- tests
import random
from itertools import permutations
assert smallest_diverse(3, 1, 0) == "aaba"
assert smallest_diverse(1, 4, 4) == "abbcbcbcc"
assert smallest_diverse(1, 3, 0) == "babb"
def brute(a, b, c):
    best = None
    for p in set(permutations('a' * a + 'b' * b + 'c' * c)):
        s = ''.join(p)
        if 'aaa' in s or 'bbb' in s or 'ccc' in s: continue
        if best is None or s < best: best = s
    return best
for _ in range(300):
    a, b, c = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
    if a + b + c == 0: continue
    exp = brute(a, b, c)
    if exp is None: continue
    assert smallest_diverse(a, b, c) == exp, (a, b, c)
smallest_diverse(100000, 100000, 100000)
print('ok')

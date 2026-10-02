def balanced_or_not(expressions, max_replacements):
    out = []
    for expr, limit in zip(expressions, max_replacements):
        open_count = 0
        need = 0
        for ch in expr:
            if ch == '<':
                open_count += 1
            elif open_count:
                open_count -= 1
            else:
                need += 1                           # an unmatched '>' must be replaced by '<>'
        out.append(1 if open_count == 0 and need <= limit else 0)
    return out

# ---- tests
import random
assert balanced_or_not(["<>>>", "<>>>>"], [2, 2]) == [1, 0]
assert balanced_or_not(["<<<><><>>"], [2]) == [0]
assert balanced_or_not(["<>", ">>"], [0, 2]) == [1, 1]
def brute(expr, limit):
    # try replacing up to `limit` '>' characters by '<>' and test balance
    from itertools import combinations
    idx = [i for i, c in enumerate(expr) if c == '>']
    def bal(s):
        o = 0
        for c in s:
            if c == '<': o += 1
            elif o: o -= 1
            else: return False
        return o == 0
    for r in range(0, min(limit, len(idx)) + 1):
        for sel in combinations(idx, r):
            t = ''.join('<>' if i in sel else c for i, c in enumerate(expr))
            if bal(t): return 1
    return 0
for _ in range(500):
    e = ''.join(random.choice('<>') for _ in range(random.randint(1, 8))); L = random.randint(0, 5)
    assert balanced_or_not([e], [L]) == [brute(e, L)], (e, L)
print('ok')

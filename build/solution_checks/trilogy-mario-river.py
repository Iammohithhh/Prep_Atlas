def river_layout(a, b, c):
    """Cells 1..a are water or platform cells; Mario starts at 0 and must reach a+1."""
    m = len(c)
    water = a - sum(c)
    # M+1 water gaps (before, between, after platforms); every gap may hold at most b-1 water cells
    if water > (m + 1) * (b - 1):
        return [-1]
    res = []
    rem = water
    for i in range(m):
        gap = min(rem, b - 1)          # push each platform as far right as allowed (lexicographically smaller)
        rem -= gap
        res.extend([0] * gap)
        res.extend([i + 1] * c[i])
    res.extend([0] * rem)              # final gap, at most b-1 by the feasibility check
    return res

# ---- tests
import random
from itertools import product
assert river_layout(7, 2, [1, 2, 1]) == [0, 1, 0, 2, 2, 0, 3]
assert river_layout(10, 5, [2]) == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
def reachable(arr, a, b):
    stand = [0] + [i + 1 for i in range(a) if arr[i] != 0] + [a + 1]
    seen = {0}; st = [0]
    while st:
        u = st.pop()
        for v in stand:
            if abs(u - v) <= b and v not in seen: seen.add(v); st.append(v)
    return a + 1 in seen
def brute(a, b, c):
    best = None
    def place(i, pos, cur):
        nonlocal best
        if i == len(c):
            arr = cur + [0] * (a - len(cur))
            if reachable(arr, a, b) and (best is None or arr < best): best = arr
            return
        for start in range(pos, a - c[i] + 1):
            place(i + 1, start + c[i], cur + [0] * (start - len(cur)) + [i + 1] * c[i])
    place(0, 0, [])
    return best if best is not None else [-1]
for _ in range(300):
    a = random.randint(1, 9); b = random.randint(1, 5)
    m = random.randint(1, min(3, a)); c = []
    left = a
    for _ in range(m):
        if left - (m - len(c) - 1) < 1: break
        x = random.randint(1, max(1, left - (m - len(c) - 1))); c.append(x); left -= x
    if len(c) != m or sum(c) > a: continue
    assert river_layout(a, b, c) == brute(a, b, c), (a, b, c)
print('ok')

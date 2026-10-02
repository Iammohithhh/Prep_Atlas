MOD = 10**9 + 7


def count_distinct_colorings(domino):
    top, bottom = domino
    n = len(top)
    i = 0
    prev = None                                  # 'V' (vertical domino) or 'H' (two stacked horizontal dominoes)
    ways = 1
    while i < n:
        if top[i] == bottom[i]:                  # vertical domino occupies one column
            kind, step = 'V', 1
        else:                                    # two horizontal dominoes cover this and the next column
            kind, step = 'H', 2
        if prev is None:
            ways = ways * (3 if kind == 'V' else 6) % MOD
        else:
            ways = ways * {('V', 'V'): 2, ('V', 'H'): 2, ('H', 'V'): 1, ('H', 'H'): 3}[(prev, kind)] % MOD
        prev = kind
        i += step
    return ways

# ---- tests
import random
from itertools import product
assert count_distinct_colorings(["ab", "ab"]) == 6
assert count_distinct_colorings(["baa", "bcc"]) == 6
assert count_distinct_colorings(["aacx", "ddcx"]) == 12
def brute(domino):
    top, bottom = domino; n = len(top)
    cells = {}
    for r, row in enumerate(domino):
        for c, ch in enumerate(row): cells[(r, c)] = ch
    pieces = sorted(set(cells.values()))
    adj = set()
    for (r, c), ch in cells.items():
        for dr, dc in ((0, 1), (1, 0)):
            q = (r + dr, c + dc)
            if q in cells and cells[q] != ch: adj.add(frozenset((ch, cells[q])))
    cnt = 0
    for colors in product(range(3), repeat=len(pieces)):
        col = dict(zip(pieces, colors))
        if all(col[a] != col[b] for a, b in map(tuple, adj)): cnt += 1
    return cnt
def random_tiling(n):
    top = []; bottom = []; i = 0; k = 0
    while len(top) < n:
        k += 1
        if random.random() < .5 or len(top) == n - 1:
            top.append(chr(96 + k)); bottom.append(chr(96 + k))
        else:
            k += 1
            top += [chr(95 + k), chr(95 + k)]; bottom += [chr(96 + k), chr(96 + k)]
    return ["".join(top), "".join(bottom)]
for _ in range(100):
    t = random_tiling(random.randint(1, 5))
    assert count_distinct_colorings(t) == brute(t), t
print('ok')

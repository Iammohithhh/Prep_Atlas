from collections import deque


def solution(table):
    if not table:
        return []
    rows, n = len(table), len(table[0])              # rows = 2n
    lines = [deque() for _ in range(rows // 2 + n - 1)]
    for i, row in enumerate(table):                  # row i starts at line i // 2 and climbs one line per symbol
        for j, ch in enumerate(row):
            lines[i // 2 + j].appendleft(ch)         # written to the left of what is already there
    out = []
    for t in range(rows):                            # output row t follows the diagonal x = t - 0.5 - line
        row = []
        for k in range(n):
            line = t // 2 + k
            idx = t - line + (len(lines[line]) - 2) // 2
            row.append(lines[line][idx])
        out.append(row)
    return out

# ---- tests
tbl = [list(r) for r in ["abc", "def", "ghi", "jkl", "mno", "pqr"]]
assert solution(tbl) == [list(r) for r in ["djp", "agm", "ekq", "bhn", "flr", "cio"]]
assert solution([]) == []
import random
for _ in range(100):
    n = random.randint(1, 6); r = 2 * n
    t = [[chr(97 + (i * n + j) % 26) for j in range(n)] for i in range(r)]
    o = solution(t)
    assert sorted(sum(o, [])) == sorted(sum(t, []))
print('ok')

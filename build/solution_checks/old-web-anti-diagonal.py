from collections import defaultdict


def can_transform(A, B):
    if len(A) != len(B) or any(len(x) != len(y) for x, y in zip(A, B)):
        return False
    da, db = defaultdict(list), defaultdict(list)
    for i, row in enumerate(A):
        for j, v in enumerate(row):
            da[i + j].append(v)
    for i, row in enumerate(B):
        for j, v in enumerate(row):
            db[i + j].append(v)
    return all(sorted(da[d]) == sorted(db[d]) for d in da)

# ---- tests
import random
from collections import deque
def reachable(A):
    n, m = len(A), len(A[0])
    start = tuple(tuple(r) for r in A)
    seen = {start}
    q = deque([start])
    while q:
        cur = q.popleft()
        for k in range(2, min(n, m) + 1):
            for r in range(n - k + 1):
                for c in range(m - k + 1):
                    g = [list(x) for x in cur]
                    for i in range(k):
                        for j in range(k):
                            g[r + i][c + j] = cur[r + j][c + i]
                    t = tuple(tuple(x) for x in g)
                    if t not in seen:
                        seen.add(t); q.append(t)
    return seen
for _ in range(60):
    n, m = random.randint(1, 3), random.randint(1, 3)
    A = [[random.randint(0, 2) for _ in range(m)] for _ in range(n)]
    R = reachable(A)
    for _ in range(8):
        B = [[random.randint(0, 2) for _ in range(m)] for _ in range(n)]
        assert can_transform(A, B) == (tuple(tuple(r) for r in B) in R), (A, B)
    B = [r[:] for r in A]
    assert can_transform(A, B)
print('ok')

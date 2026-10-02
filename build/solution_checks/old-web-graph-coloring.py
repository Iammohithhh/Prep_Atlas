def can_color(n, edges, m):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        if a == b:
            return False
        adj[a].add(b)
        adj[b].add(a)
    order = sorted(range(n), key=lambda v: -len(adj[v]))      # colour crowded vertices first
    color = {}

    def go(i):
        if i == n:
            return True
        v = order[i]
        used = {color[u] for u in adj[v] if u in color}
        tried_new = False
        for c in range(m):
            if c in used:
                continue
            if c not in color.values():            # symmetry breaking: open at most one new colour
                if tried_new:
                    continue
                tried_new = True
            color[v] = c
            if go(i + 1):
                return True
            del color[v]
        return False

    return go(0)

# ---- tests
import random
from itertools import product
assert can_color(3, [(0, 1), (1, 2), (2, 0)], 3)
assert not can_color(3, [(0, 1), (1, 2), (2, 0)], 2)
assert can_color(0, [], 1)
assert not can_color(2, [(0, 1)], 0) and can_color(0, [], 0)
def brute(n, edges, m):
    return any(all(col[a] != col[b] for a, b in edges) for col in product(range(m), repeat=n))
for _ in range(400):
    n = random.randint(0, 6)
    edges = [(random.randrange(n), random.randrange(n)) for _ in range(random.randint(0, 9))] if n else []
    m = random.randint(0, 4)
    assert can_color(n, edges, m) == brute(n, edges, m), (n, edges, m)
print('ok')

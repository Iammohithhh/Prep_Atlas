import random
from itertools import combinations

def getMaximumEdges(n, frm, to, special, max_conn):
    parent = list(range(n + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in zip(frm, to):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    size = {}
    for v in range(1, n + 1):
        r = find(v)
        size[r] = size.get(r, 0) + 1
    sp_roots = {find(s) for s in special}
    sp_sizes = sorted((size[r] for r in sp_roots), reverse=True)
    free = sum(sz for r, sz in size.items() if r not in sp_roots)
    # group the special components into chunks of max_conn (largest first); free vertices join the largest group
    groups = [sum(sp_sizes[i:i + max_conn]) for i in range(0, len(sp_sizes), max_conn)]
    if groups:
        groups[0] += free
    else:
        groups = [free]
    total = sum(g * (g - 1) // 2 for g in groups)
    return total - len(frm)

def valid(n, edges, special, m):
    parent = list(range(n + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        parent[find(a)] = find(b)
    cnt = {}
    for s in special:
        cnt[find(s)] = cnt.get(find(s), 0) + 1
    return all(c <= m for c in cnt.values())

def brute(n, frm, to, special, m):
    existing = set(tuple(sorted(e)) for e in zip(frm, to))
    pairs = [p for p in combinations(range(1, n + 1), 2) if p not in existing]
    best = 0
    for mask in range(1 << len(pairs)):
        add = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        if len(add) <= best:
            continue
        if valid(n, list(existing) + add, special, m):
            best = len(add)
    return best

assert getMaximumEdges(4, [1], [2], [1, 3], 1) == 2
for _ in range(120):
    n = random.randint(2, 6)
    allp = list(combinations(range(1, n + 1), 2))
    k = random.randint(1, min(3, n))
    special = random.sample(range(1, n + 1), k)
    m = random.randint(1, k)
    random.shuffle(allp)
    edges = []
    for p in allp[:random.randint(0, 3)]:
        edges.append(p)
        if not valid(n, edges, special, 1):
            edges.pop()
    frm = [e[0] for e in edges]
    to = [e[1] for e in edges]
    assert getMaximumEdges(n, frm, to, special, m) == brute(n, frm, to, special, m), (n, edges, special, m)
print('ok')

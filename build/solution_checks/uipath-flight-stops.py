import random
from math import inf
from collections import defaultdict

def getOptimalFlightRates(nodes, frm, to, wt, queries):
    by_src = defaultdict(list)
    for idx, (s, d, k) in enumerate(queries):
        by_src[s].append((idx, d, k))
    res = [-1] * len(queries)
    for s, qs in by_src.items():
        K = max(k for _, _, k in qs) + 1          # at most k + 1 edges
        cur = [inf] * nodes
        cur[s] = 0
        best = [cur[:]]
        for t in range(K):
            nxt = cur[:]
            for u, v, w in zip(frm, to, wt):
                if cur[u] + w < nxt[v]:
                    nxt[v] = cur[u] + w
            cur = nxt
            best.append(cur[:])
        for idx, d, k in qs:
            c = best[k + 1][d]
            res[idx] = -1 if c == inf else c
    return res

def brute(nodes, frm, to, wt, q):
    s, d, k = q
    best = inf
    def dfs(u, edges, cost):
        nonlocal best
        if u == d:
            best = min(best, cost)
        if edges == k + 1:
            return
        for a, b, w in zip(frm, to, wt):
            if a == u:
                dfs(b, edges + 1, cost + w)
    dfs(s, 0, 0)
    return -1 if best == inf else best

ex = getOptimalFlightRates(5, [0, 1, 2, 2, 0, 2, 4], [1, 2, 3, 0, 2, 4, 2], [100, 150, 70, 300, 400, 200, 120], [[0, 4, 2], [0, 3, 1], [1, 3, 0]])
assert ex == [450, 470, -1], ex
for _ in range(200):
    n = random.randint(2, 5)
    m = random.randint(1, 8)
    fr = [random.randrange(n) for _ in range(m)]
    to = [random.randrange(n) for _ in range(m)]
    wt = [random.randint(1, 9) for _ in range(m)]
    qs = [[random.randrange(n), random.randrange(n), random.randint(0, 3)] for _ in range(4)]
    out = getOptimalFlightRates(n, fr, to, wt, qs)
    for q, o in zip(qs, out):
        if q[0] == q[1]:
            continue
        assert o == brute(n, fr, to, wt, q), (n, fr, to, wt, q, o)
print('ok')

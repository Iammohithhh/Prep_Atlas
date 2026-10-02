from collections import deque


def energy_nodes(n, m, k, energy, edges):
    if n == 1:
        return 0
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    # multi-source BFS from the booster nodes and from node n (the target acts as a terminal)
    sources = set(energy) | {n}
    owner = [0] * (n + 1)
    dist = [-1] * (n + 1)
    dq = deque()
    for s in sources:
        owner[s] = s
        dist[s] = 0
        dq.append(s)
    while dq:
        u = dq.popleft()
        for w in adj[u]:
            if dist[w] < 0:
                dist[w] = dist[u] + 1
                owner[w] = owner[u]
                dq.append(w)
    # an edge between two different regions links their sources with cost d[u] + 1 + d[v]
    links = []
    for u, v in edges:
        if dist[u] >= 0 and dist[v] >= 0 and owner[u] != owner[v]:
            links.append((dist[u] + 1 + dist[v], owner[u], owner[v]))
    links.sort()
    parent = {s: s for s in sources}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    start = 1                                   # node 1 is guaranteed to be a booster
    for w, a, b in links:                       # Kruskal: first time 1 and n join gives the bottleneck
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
        if find(start) == find(n):
            return w
    return 0 if find(start) == find(n) else -1

# ---- tests
import random
assert energy_nodes(5, 4, 3, [1, 2, 5], [(1, 2), (2, 3), (3, 4), (4, 5)]) == 3
def brute(n, m, k, energy, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    boosters = set(energy)
    for P in range(0, n + 1):
        seen = {(1, P)}; st = [(1, P)]
        while st:
            u, p = st.pop()
            if u == n: return P
            for w in adj[u]:
                if p == 0: continue
                np_ = P if w in boosters else p - 1
                if (w, np_) not in seen: seen.add((w, np_)); st.append((w, np_))
    return -1
for _ in range(500):
    n = random.randint(2, 9)
    es = set()
    for _ in range(random.randint(0, 12)):
        u, v = random.randint(1, n), random.randint(1, n)
        if u != v: es.add((min(u, v), max(u, v)))
    edges = sorted(es)
    others = [i for i in range(2, n + 1) if random.random() < .3]
    energy = [1] + others
    assert energy_nodes(n, len(edges), len(energy), energy, edges) == brute(n, len(edges), len(energy), energy, edges), (n, energy, edges)
print('ok')

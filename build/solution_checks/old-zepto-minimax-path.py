def path_value(n, m, s, e, edge, a):
    if s == e:
        return 0
    es = sorted(((abs(a[u - 1] - a[v - 1]), u, v) for u, v in edge))
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for w, u, v in es:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            if find(s) == find(e):
                return w
    return -1

# ---- tests
import random, heapq
assert path_value(5, 7, 2, 5, [(1, 2), (2, 3), (3, 4), (4, 5), (1, 3), (1, 4), (1, 5)], [20, 23, 21, 45, 21]) == 2
def dijkstra(n, s, e, edge, a):
    adj = [[] for _ in range(n + 1)]
    for u, v in edge:
        w = abs(a[u - 1] - a[v - 1])
        adj[u].append((v, w)); adj[v].append((u, w))
    dist = [None] * (n + 1)
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if dist[u] is not None:
            continue
        dist[u] = d
        for v, w in adj[u]:
            if dist[v] is None:
                heapq.heappush(pq, (max(d, w), v))
    return -1 if dist[e] is None else dist[e]
for _ in range(400):
    n = random.randint(1, 8)
    edge = [(random.randint(1, n), random.randint(1, n)) for _ in range(random.randint(0, 10))]
    edge = [(u, v) for u, v in edge if u != v]
    a = [random.randint(1, 20) for _ in range(n)]
    s, e = random.randint(1, n), random.randint(1, n)
    assert path_value(n, len(edge), s, e, edge, a) == dijkstra(n, s, e, edge, a)
print('ok')

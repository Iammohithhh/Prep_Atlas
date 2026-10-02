from collections import deque


def shortest_path(n, edges, source, target):
    if source == target:
        return 0
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    dist = [-1] * n
    dist[source] = 0
    q = deque([source])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                if v == target:
                    return dist[v]
                q.append(v)
    return -1

# ---- tests
import random
assert shortest_path(1, [], 0, 0) == 0
assert shortest_path(4, [(0, 1), (1, 2)], 0, 3) == -1
assert shortest_path(5, [(0, 1), (1, 2), (2, 4), (0, 3), (3, 4)], 0, 4) == 2
def floyd(n, edges, s, t):
    INF = 10 ** 9
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for a, b in edges:
        if a != b:
            d[a][b] = d[b][a] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return -1 if d[s][t] >= INF else d[s][t]
for _ in range(300):
    n = random.randint(1, 7)
    edges = [(random.randrange(n), random.randrange(n)) for _ in range(random.randint(0, 9))]
    s, t = random.randrange(n), random.randrange(n)
    assert shortest_path(n, edges, s, t) == floyd(n, edges, s, t)
print('ok')

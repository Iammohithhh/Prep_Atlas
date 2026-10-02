import random
INF = float('inf')

def dijkstra(W, src, n):
    d = [INF] * n; d[src] = 0; done = [False] * n
    for _ in range(n):
        u = -1; best = INF
        for i in range(n):
            if not done[i] and d[i] < best: best, u = d[i], i
        if u < 0: break
        done[u] = True
        row = W[u]
        for v in range(n):
            w = row[v]
            if w != -1 and d[u] + w < d[v]: d[v] = d[u] + w
    return d

def transpose(W):
    return [list(c) for c in zip(*W)]

def minCost(n, B, P, S, E):
    S -= 1; E -= 1
    best = INF
    for first, second in ((B, P), (P, B)):
        d1 = dijkstra(first, S, n)
        d2 = dijkstra(transpose(second), E, n)     # cost from I to E using second mode
        for i in range(n):
            if i != S and i != E: best = min(best, d1[i] + d2[i])
    return -1 if best == INF else best

def brute(n, B, P, S, E):
    # Floyd-Warshall per mode
    def fw(W):
        d = [[INF if W[i][j] == -1 else W[i][j] for j in range(n)] for i in range(n)]
        for i in range(n): d[i][i] = 0
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j])
        return d
    dB, dP = fw(B), fw(P)
    S -= 1; E -= 1
    best = INF
    for i in range(n):
        if i in (S, E): continue
        best = min(best, dB[S][i] + dP[i][E], dP[S][i] + dB[i][E])
    return -1 if best == INF else best

B = [[-1, 1, 2], [3, -1, 4], [5, 6, -1]]
P = [[-1, 6, 5], [1, -1, 4], [3, 2, -1]]
assert minCost(3, B, P, 1, 2) == 4
for _ in range(200):
    n = random.randint(3, 6)
    mk = lambda: [[-1 if i == j or random.random() < 0.3 else random.randint(1, 9) for j in range(n)] for i in range(n)]
    B, P = mk(), mk()
    S, E = random.sample(range(1, n + 1), 2)
    assert minCost(n, B, P, S, E) == brute(n, B, P, S, E)
print('ok')

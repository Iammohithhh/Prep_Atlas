def path_minimum_sum(n, weight, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent = list(range(n))
    size = [1] * n
    active = [False] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    for u in sorted(range(n), key=lambda i: -weight[i]):
        active[u] = True
        for v in adj[u]:
            if active[v]:
                ru, rv = find(u), find(v)
                if ru != rv:
                    total += weight[u] * size[ru] * size[rv]    # new pairs whose path minimum is weight[u]
                    if size[ru] < size[rv]:
                        ru, rv = rv, ru
                    parent[rv] = ru
                    size[ru] += size[rv]
    return total

# ---- tests
import random
assert path_minimum_sum(4, [6, 3, 7, 5], [[0, 1], [1, 3], [0, 2]]) == 21
assert path_minimum_sum(5, [6, 1, 2, 5, 3], [[0, 1], [1, 2], [0, 4], [2, 3]]) == 13
def brute(n, w, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b); adj[b].append(a)
    total = 0
    for s in range(n):
        stack = [(s, -1, w[s])]
        while stack:
            u, p, mn = stack.pop()
            if u > s:
                total += mn
            for v in adj[u]:
                if v != p:
                    stack.append((v, u, min(mn, w[v])))
    return total
for _ in range(300):
    n = random.randint(2, 9)
    edges = [[random.randint(0, i - 1), i] for i in range(1, n)]
    w = [random.randint(1, 6) for _ in range(n)]
    assert path_minimum_sum(n, w, edges) == brute(n, w, edges)
print('ok')

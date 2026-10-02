from collections import deque


def is_bipartite(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        if a == b:
            return False                      # a self-loop can never join two different teams
        adj[a].append(b)
        adj[b].append(a)
    color = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True

# ---- tests
import random
from itertools import product
assert is_bipartite(0, [])
assert is_bipartite(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
assert not is_bipartite(3, [(0, 1), (1, 2), (2, 0)])
assert not is_bipartite(2, [(1, 1)])
def brute(n, edges):
    for col in product((0, 1), repeat=n):
        if all(col[a] != col[b] for a, b in edges):
            return True
    return False
for _ in range(400):
    n = random.randint(0, 7)
    edges = [(random.randrange(n), random.randrange(n)) for _ in range(random.randint(0, 9))] if n else []
    assert is_bipartite(n, edges) == brute(n, edges), (n, edges)
print('ok')

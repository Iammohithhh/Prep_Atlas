MOD = 10**9 + 7


def count_tree_paths(tree_nodes, tree_from, tree_to):
    n = tree_nodes
    adj = [[] for _ in range(n)]
    for u, v in zip(tree_from, tree_to):
        adj[u].append(v)
        adj[v].append(u)
    parent = [-1] * n
    order = []
    stack = [0]
    seen = [False] * n
    seen[0] = True
    while stack:
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if not seen[w]:
                seen[w] = True
                parent[w] = u
                stack.append(w)
    size = [1] * n
    for u in reversed(order):
        if parent[u] >= 0:
            size[parent[u]] += size[u]
    def c2(x):
        return x * (x - 1) // 2
    on_path = 0                                      # triples lying on one simple path, counted by their middle vertex
    for v in range(n):
        parts = [size[w] for w in adj[v] if parent[w] == v]
        if parent[v] >= 0:
            parts.append(n - size[v])
        on_path += c2(n - 1) - sum(c2(s) for s in parts)
    total = n * (n - 1) * (n - 2) // 6
    return (total - on_path) % MOD

# ---- tests
import random
from itertools import combinations
assert count_tree_paths(5, [1, 1, 0, 0], [0, 2, 3, 4]) == 2
assert count_tree_paths(1, [], []) == 0
def brute(n, tf, tt):
    adj = [set() for _ in range(n)]
    for u, v in zip(tf, tt): adj[u].add(v); adj[v].add(u)
    def path(a, b):
        prev = {a: None}; q = [a]
        for u in q:
            for w in adj[u]:
                if w not in prev: prev[w] = u; q.append(w)
        p = []; x = b
        while x is not None: p.append(x); x = prev[x]
        return set(p)
    cnt = 0
    for t in combinations(range(n), 3):
        if not any(set(t) <= path(x, y) for x, y in combinations(t, 2)): cnt += 1
    return cnt
for _ in range(300):
    n = random.randint(1, 10)
    tf = [random.randint(0, i - 1) for i in range(1, n)]; tt = list(range(1, n))
    assert count_tree_paths(n, tf, tt) == brute(n, tf, tt)
print('ok')

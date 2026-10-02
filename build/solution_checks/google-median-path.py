def solve(n, c, edges):
    """Sum of medians of every odd-length (odd number of nodes) path that starts at node 1."""
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    vals = sorted(set(c))
    rank = {v: i + 1 for i, v in enumerate(vals)}   # compressed values, 1-based
    m = len(vals)
    tree = [0] * (m + 1)                             # Fenwick tree over value counts
    log = 1
    while (1 << log) <= m:
        log += 1

    def update(i, d):
        while i <= m:
            tree[i] += d
            i += i & -i

    def kth(k):                                      # smallest rank whose prefix count >= k
        pos = 0
        for b in range(log, -1, -1):
            nxt = pos + (1 << b)
            if nxt <= m and tree[nxt] < k:
                pos = nxt
                k -= tree[nxt]
        return pos + 1

    total = 0
    # iterative DFS: stack entries (node, parent, depth, state); state 0 = enter, 1 = leave
    stack = [(1, 0, 1, 0)]
    while stack:
        u, p, depth, state = stack.pop()
        if state == 1:
            update(rank[c[u - 1]], -1)
            continue
        update(rank[c[u - 1]], 1)
        if depth % 2 == 1:                           # odd number of nodes on the path
            total += vals[kth((depth + 1) // 2) - 1]
        stack.append((u, p, depth, 1))
        for w in adj[u]:
            if w != p:
                stack.append((w, u, depth + 1, 0))
    return total

# ---- tests
import random
assert solve(5, [7, 6, 9, 10, 1], [(1, 2), (2, 3), (1, 4), (2, 5)]) == 20
assert solve(6, [1, 2, 4, 3, 1, 5], [(1, 4), (4, 2), (4, 3), (4, 5), (1, 6)]) == 7
assert solve(1, [5], []) == 5
def brute(n, c, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    tot = 0
    def go(u, p, path):
        nonlocal tot
        path = path + [c[u - 1]]
        if len(path) % 2: tot += sorted(path)[len(path) // 2]
        for w in adj[u]:
            if w != p: go(w, u, path)
    go(1, 0, [])
    return tot
for _ in range(300):
    n = random.randint(1, 12)
    edges = [(random.randint(1, i), i + 1) for i in range(1, n)]
    c = [random.randint(1, 6) for _ in range(n)]
    assert solve(n, c, edges) == brute(n, c, edges)
# deep chain, no recursion errors
n = 100000
solve(n, [i % 1000 + 1 for i in range(n)], [(i, i + 1) for i in range(1, n)])
print('ok')

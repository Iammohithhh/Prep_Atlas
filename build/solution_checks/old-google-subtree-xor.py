def maximum_sum(n, edges, a, k):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    gain = [0] + [(x ^ k) - x for x in a]          # change in the sum if node v is XOR-ed with k
    parent = [0] * (n + 1)
    order = []
    stack = [1]
    seen = [False] * (n + 1)
    seen[1] = True
    while stack:
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if not seen[w]:
                seen[w] = True
                parent[w] = u
                stack.append(w)
    s = gain[:]                                    # s[v] = total gain of the subtree of v (rooted at 1)
    for u in reversed(order):
        if parent[u]:
            s[parent[u]] += s[u]
    total_gain = s[1]
    best = max(0, total_gain)                      # do nothing, or XOR the whole tree
    for v in range(2, n + 1):
        best = max(best, s[v], total_gain - s[v])  # one side of the edge (v, parent[v])
    return sum(a) + best

# ---- tests
import random
assert maximum_sum(3, [(1, 2), (1, 3)], [1, 1, 3], 3) == 7
assert maximum_sum(4, [(1, 2), (2, 3), (2, 4)], [1, 1, 1, 1], 3) == 8
def brute(n, edges, a, k):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    best = sum(a)
    for r in range(1, n + 1):
        par = {r: 0}; order = [r]
        for u in order:
            for w in adj[u]:
                if w not in par: par[w] = u; order.append(w)
        for x in range(1, n + 1):
            sub = {x}; ch = True
            while ch:
                ch = False
                for u in range(1, n + 1):
                    if u not in sub and par.get(u) in sub: sub.add(u); ch = True
            best = max(best, sum(a[i - 1] ^ k if i in sub else a[i - 1] for i in range(1, n + 1)))
    return best
for _ in range(300):
    n = random.randint(1, 8)
    edges = [(random.randint(1, i), i + 1) for i in range(1, n)]
    a = [random.randint(0, 15) for _ in range(n)]; k = random.randint(0, 15)
    assert maximum_sum(n, edges, a, k) == brute(n, edges, a, k)
print('ok')

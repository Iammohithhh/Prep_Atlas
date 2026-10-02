def get_min_inversions(g_nodes, g_from, g_to):
    adj = [[] for _ in range(g_nodes + 1)]
    for u, v in zip(g_from, g_to):
        adj[u].append((v, 0))        # edge u -> v is already pointing "down" when we walk u to v
        adj[v].append((u, 1))        # walking v to u goes against the edge: needs an inversion
    # cost for root 1 = number of edges pointing toward the root; then reroot
    cost = [0] * (g_nodes + 1)
    parent = [0] * (g_nodes + 1)
    order = []
    stack = [1]
    seen = [False] * (g_nodes + 1)
    seen[1] = True
    while stack:
        u = stack.pop()
        order.append(u)
        for w, c in adj[u]:
            if not seen[w]:
                seen[w] = True
                parent[w] = u
                stack.append(w)
    base = 0
    for u in order:
        for w, c in adj[u]:
            if parent[w] == u:
                base += c
    cost[1] = base
    for u in order:
        for w, c in adj[u]:
            if parent[w] == u:
                # moving the root from u to w flips the direction cost of edge (u, w)
                cost[w] = cost[u] + (1 if c == 0 else -1)
    return min(cost[1:])

# ---- tests
import random
assert get_min_inversions(4, [1, 2, 3], [4, 4, 4]) == 2
assert get_min_inversions(3, [2, 2], [1, 3]) == 0
def brute(n, gf, gt):
    best = n
    for root in range(1, n + 1):
        adj = [[] for _ in range(n + 1)]
        for u, v in zip(gf, gt): adj[u].append((v, 0)); adj[v].append((u, 1))
        seen = {root}; st = [root]; tot = 0
        while st:
            u = st.pop()
            for w, c in adj[u]:
                if w not in seen: seen.add(w); tot += c; st.append(w)
        best = min(best, tot)
    return best
for _ in range(500):
    n = random.randint(2, 9)
    gf, gt = [], []
    for i in range(2, n + 1):
        p = random.randint(1, i - 1)
        if random.random() < .5: gf.append(p); gt.append(i)
        else: gf.append(i); gt.append(p)
    assert get_min_inversions(n, gf, gt) == brute(n, gf, gt)
print('ok')

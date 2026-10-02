def get_maximum_efficiency(n, connect_from, connect_to, val, k):
    adj = [[] for _ in range(n + 1)]
    for u, v in zip(connect_from, connect_to):
        adj[u].append(v)
        adj[v].append(u)
    parent = [0] * (n + 1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:                                     # iterative DFS order from the root
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if w != parent[u]:
                parent[w] = u
                stack.append(w)
    best = [0] * (n + 1)
    keep_sum = [0] * (n + 1)                         # value of node + best of its children
    for u in reversed(order):
        keep = val[u - 1] + keep_sum[u]
        best[u] = max(keep, -k)                      # keep the subtree, or cut it for a cost of k
        if parent[u] > 0:
            keep_sum[parent[u]] += best[u]
    return best[1]

# ---- tests
import random
assert get_maximum_efficiency(4, [1, 2, 3], [2, 3, 4], [3, -7, -8, -9], 5) == -2
def brute(n, cf, ct, val, k):
    parent = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    for u, v in zip(cf, ct): adj[u].append(v); adj[v].append(u)
    sub = {}
    def dfs(u, p):
        s = {u}
        for w in adj[u]:
            if w != p: s |= dfs(w, u)
        sub[u] = s
        return s
    dfs(1, 0)
    best = -10**18
    for mask in range(1 << n):
        cut = [i + 1 for i in range(n) if mask >> i & 1]
        # operations are applied one by one; ancestors already removed make a cut redundant, count only minimal cuts
        removed = set()
        ops = 0
        for u in sorted(cut, key=lambda x: len(sub[x]), reverse=True):
            if u in removed: continue
            removed |= sub[u]; ops += 1
        rem = sum(val[i - 1] for i in range(1, n + 1) if i not in removed)
        best = max(best, rem - k * ops)
    return best
for _ in range(300):
    n = random.randint(1, 8)
    cf = [random.randint(1, i) for i in range(1, n)]; ct = [i + 1 for i in range(1, n)]
    val = [random.randint(-9, 9) for _ in range(n)]; k = random.randint(0, 10)
    assert get_maximum_efficiency(n, cf, ct, val, k) == brute(n, cf, ct, val, k), (n, cf, ct, val, k)
print('ok')

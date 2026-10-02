def get_min_leaves_to_remove(n, frm, to, weight, arr):
    adj = [[] for _ in range(n + 1)]
    for a, b, w in zip(frm, to, weight):
        adj[a].append((b, w))
        adj[b].append((a, w))
    removed = 0
    stack = [(1, 0, 0)]                      # node, parent, best ancestor-to-node path sum (>= 0)
    while stack:
        u, p, d = stack.pop()
        for v, w in adj[u]:
            if v == p:
                continue
            nd = max(0, d + w)
            if nd > arr[v - 1]:
                # the whole subtree of v has to go
                sub = [(v, u)]
                while sub:
                    x, px = sub.pop()
                    removed += 1
                    for y, _ in adj[x]:
                        if y != px:
                            sub.append((y, x))
            else:
                stack.append((v, u, nd))
    return removed

# ---- tests
import random
def brute(n, frm, to, weight, arr):
    par = {1: 0}
    adj = [[] for _ in range(n + 1)]
    for a, b, w in zip(frm, to, weight):
        adj[a].append((b, w)); adj[b].append((a, w))
    order = [1]; wt = {1: 0}
    for u in order:
        for v, w in adj[u]:
            if v not in par:
                par[v] = u; wt[v] = w; order.append(v)
    best_keep = 0
    nodes = list(range(2, n + 1))
    for mask in range(1 << len(nodes)):
        keep = {1} | {nodes[i] for i in range(len(nodes)) if mask >> i & 1}
        if any(par[v] not in keep for v in keep if v != 1):
            continue                          # kept set must stay connected to the root
        ok = True
        for y in keep:
            s = 0; x = y
            while x != 1:
                s += wt[x]; x = par[x]
                if s > arr[y - 1]:
                    ok = False
            if not ok:
                break
        if ok:
            best_keep = max(best_keep, len(keep))
    return n - best_keep
assert brute(5, [1, 1, 3, 3], [2, 3, 4, 5], [8, 5, 2, 7], [12, 2, 27, 11, 1]) == 2
assert get_min_leaves_to_remove(5, [1, 1, 3, 3], [2, 3, 4, 5], [8, 5, 2, 7], [12, 2, 27, 11, 1]) == 2
for _ in range(400):
    n = random.randint(1, 9)
    frm = [random.randint(1, i) for i in range(1, n)]
    to = list(range(2, n + 1))
    weight = [random.randint(-3, 6) for _ in range(n - 1)]
    arr = [random.randint(1, 9) for _ in range(n)]
    assert get_min_leaves_to_remove(n, frm, to, weight, arr) == brute(n, frm, to, weight, arr), (n, frm, to, weight, arr)
print('ok')

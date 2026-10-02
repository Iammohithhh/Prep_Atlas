def best_sum_any_tree_path(parent, values):
    n = len(parent)
    children = [[] for _ in range(n)]
    root = 0
    for i, p in enumerate(parent):
        if p == -1:
            root = i
        else:
            children[p].append(i)
    order = []
    stack = [root]
    while stack:
        u = stack.pop()
        order.append(u)
        stack.extend(children[u])
    down = [0] * n                                  # best downward path sum starting at u
    best = float('-inf')
    for u in reversed(order):
        gains = sorted((max(0, down[c]) for c in children[u]), reverse=True)
        top1 = gains[0] if gains else 0
        top2 = gains[1] if len(gains) > 1 else 0
        down[u] = values[u] + top1
        best = max(best, values[u] + top1 + top2)
    return best

# ---- tests
import random
assert best_sum_any_tree_path([-1, 0, 1, 2, 0], [-2, 10, 10, -3, 10]) == 28
def brute(parent, values):
    n = len(parent); adj = [[] for _ in range(n)]
    for i, p in enumerate(parent):
        if p >= 0: adj[i].append(p); adj[p].append(i)
    best = float('-inf')
    def dfs(u, seen, total):
        nonlocal best
        best = max(best, total)
        for w in adj[u]:
            if w not in seen: dfs(w, seen | {w}, total + values[w])
    for s in range(n): dfs(s, {s}, values[s])
    return best
for _ in range(400):
    n = random.randint(1, 9)
    parent = [-1] + [random.randint(0, i - 1) for i in range(1, n)]
    values = [random.randint(-9, 9) for _ in range(n)]
    assert best_sum_any_tree_path(parent, values) == brute(parent, values)
print('ok')

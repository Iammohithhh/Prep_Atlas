def best_sum_downward_tree_path(parent, values):
    n = len(parent)
    children = [[] for _ in range(n)]
    root = 0
    for i, p in enumerate(parent):
        if p == -1:
            root = i
        else:
            children[p].append(i)
    best_end = [0] * n                               # best downward path sum ending at u
    best = float('-inf')
    stack = [root]
    best_end[root] = values[root]
    while stack:
        u = stack.pop()
        best = max(best, best_end[u])
        for c in children[u]:
            best_end[c] = values[c] + max(0, best_end[u])
            stack.append(c)
    return best

# ---- tests
import random
assert best_sum_downward_tree_path([-1, 0, 1, 2, 0], [-2, 10, 10, -3, 10]) == 20
def brute(parent, values):
    n = len(parent); best = float('-inf')
    for v in range(n):
        total = 0; u = v
        while u != -1:
            total += values[u]; best = max(best, total); u = parent[u]
    return best
for _ in range(400):
    n = random.randint(1, 9)
    parent = [-1] + [random.randint(0, i - 1) for i in range(1, n)]
    values = [random.randint(-9, 9) for _ in range(n)]
    assert best_sum_downward_tree_path(parent, values) == brute(parent, values)
print('ok')

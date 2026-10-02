import random
from itertools import product

def findMinChanges(dep):
    n = len(dep)
    d = [x - 1 for x in dep]
    state = [0] * n          # 0 unvisited, 1 on current walk, 2 finished
    comps = 0
    has_self = False
    for s in range(n):
        if state[s]:
            continue
        path = []
        u = s
        while state[u] == 0:
            state[u] = 1
            path.append(u)
            u = d[u]
        if state[u] == 1:    # closed a new cycle
            comps += 1
            if d[u] == u:
                has_self = True
        for v in path:
            state[v] = 2
    return comps - 1 if has_self else comps

def valid(d):
    n = len(d)
    roots = [i for i in range(n) if d[i] == i]
    if len(roots) != 1:
        return False
    for s in range(n):
        u = s
        for _ in range(n + 1):
            if u == roots[0]:
                break
            u = d[u]
        else:
            return False
    return True

def brute(dep):
    n = len(dep)
    best = n
    for cand in product(range(n), repeat=n):
        if valid(list(cand)):
            best = min(best, sum(1 for a, b in zip(cand, dep) if a != b - 1))
    return best

assert findMinChanges([1, 2, 3, 4]) == 3
assert findMinChanges([2, 3, 3, 4]) == 1
for _ in range(300):
    n = random.randint(1, 6)
    dep = [random.randint(1, n) for _ in range(n)]
    assert findMinChanges(dep) == brute(dep), dep
print('ok')

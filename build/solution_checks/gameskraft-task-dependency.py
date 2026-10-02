def find_min_changes(task_dependency):
    n = len(task_dependency)
    nxt = [d - 1 for d in task_dependency]
    state = [0] * n                      # 0 = unvisited, 1 = on the current walk, 2 = done
    self_loops = other_cycles = 0
    for start in range(n):
        if state[start]:
            continue
        path = []
        v = start
        while state[v] == 0:
            state[v] = 1
            path.append(v)
            v = nxt[v]
        if state[v] == 1:                # found a new cycle in this walk
            if v == nxt[v]:
                self_loops += 1
            else:
                other_cycles += 1
        for u in path:
            state[u] = 2
    cycles = self_loops + other_cycles
    return cycles - 1 if self_loops else cycles

# ---- tests
import random
assert find_min_changes([2, 3, 3, 4]) == 1
assert find_min_changes([1, 2, 3, 4]) == 3
assert find_min_changes([1]) == 0
assert find_min_changes([2, 1]) == 1
def valid(dep):
    n = len(dep)
    loops = [i for i in range(n) if dep[i] - 1 == i]
    if len(loops) != 1: return False
    root = loops[0]
    for i in range(n):
        v = i
        for _ in range(n + 1):
            if v == root: break
            v = dep[v] - 1
        else:
            return False
    return True
def brute(dep):
    n = len(dep); best = n
    from itertools import product
    for cand in product(range(1, n + 1), repeat=n):
        if valid(cand):
            best = min(best, sum(1 for a, b in zip(cand, dep) if a != b))
    return best
for _ in range(300):
    n = random.randint(1, 6)
    dep = [random.randint(1, n) for _ in range(n)]
    assert find_min_changes(dep) == brute(dep), dep
print('ok')

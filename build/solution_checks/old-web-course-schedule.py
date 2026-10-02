from collections import deque


def find_order(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for course, pre in prerequisites:         # pre must be taken before course
        adj[pre].append(course)
        indeg[course] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == num_courses else []

# ---- tests
import random
from itertools import permutations
assert find_order(2, [[1, 0]]) == [0, 1]
assert find_order(2, [[1, 0], [0, 1]]) == []
assert find_order(1, []) == [0]
def valid(order, n, pre):
    pos = {c: i for i, c in enumerate(order)}
    return len(order) == n and len(pos) == n and all(pos[p] < pos[c] for c, p in pre)
for _ in range(400):
    n = random.randint(1, 6)
    pre = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 7))]
    out = find_order(n, pre)
    exists = any(valid(list(p), n, pre) for p in permutations(range(n)))
    assert bool(out) == exists
    if out:
        assert valid(out, n, pre)
print('ok')

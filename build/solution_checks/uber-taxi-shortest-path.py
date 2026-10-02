from collections import deque


def shortest_taxi_path(grid, taxi_stands, passenger):
    m, n = len(grid), len(grid[0])
    prev = {}
    dq = deque()
    for r, c in taxi_stands:                     # multi-source BFS
        if grid[r][c] == 0 and (r, c) not in prev:
            prev[(r, c)] = None
            dq.append((r, c))
    target = tuple(passenger)
    while dq:
        r, c = dq.popleft()
        if (r, c) == target:
            path = []
            cur = target
            while cur is not None:
                path.append(list(cur))
                cur = prev[cur]
            return path[::-1]
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in prev:
                prev[(nr, nc)] = (r, c)
                dq.append((nr, nc))
    return []

# ---- tests
import random
g = [[0, 1, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1], [0, 0, 0, 0]]
assert shortest_taxi_path(g, [[0, 0], [3, 3]], [1, 3]) == [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3]]
assert shortest_taxi_path([[0, 1], [1, 0]], [[0, 0]], [1, 1]) == []
def brute_len(grid, stands, p):
    m, n = len(grid), len(grid[0]); best = None
    for s in stands:
        dist = {tuple(s): 0}; q = [tuple(s)]
        for u in q:
            for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
                v = (u[0]+dr, u[1]+dc)
                if 0<=v[0]<m and 0<=v[1]<n and grid[v[0]][v[1]]==0 and v not in dist:
                    dist[v] = dist[u]+1; q.append(v)
        if tuple(p) in dist and (best is None or dist[tuple(p)] < best): best = dist[tuple(p)]
    return best
for _ in range(300):
    m, n = random.randint(1, 5), random.randint(1, 5)
    grid = [[1 if random.random() < .3 else 0 for _ in range(n)] for _ in range(m)]
    roads = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == 0]
    if not roads: continue
    p = list(random.choice(roads)); stands = [list(random.choice(roads)) for _ in range(2)]
    res = shortest_taxi_path(grid, stands, p); b = brute_len(grid, stands, p)
    if b is None: assert res == []
    else:
        assert len(res) == b + 1 and res[0] in stands and res[-1] == p
        for a, c in zip(res, res[1:]):
            assert abs(a[0]-c[0]) + abs(a[1]-c[1]) == 1 and grid[c[0]][c[1]] == 0
print('ok')

from collections import deque
import random

def shortestRescue(input1, input2, input3):
    n, m, g = input1, input2, input3
    start = next((i, j) for i in range(n) for j in range(m) if g[i][j] == 1)
    dist = {start: 1}                      # path length counts cells
    q = deque([start])
    while q:
        x, y = q.popleft()
        if g[x][y] == 2: return dist[(x, y)]
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            a, b = x + dx, y + dy
            if 0 <= a < n and 0 <= b < m and g[a][b] != -1 and (a, b) not in dist:
                dist[(a, b)] = dist[(x, y)] + 1
                q.append((a, b))
    return -1

def brute(n, m, g):
    # Bellman-Ford style relaxation
    INF = 10**9
    d = [[INF]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if g[i][j] == 1: d[i][j] = 1
    for _ in range(n*m):
        for i in range(n):
            for j in range(m):
                if g[i][j] == -1: continue
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    a, b = i+dx, j+dy
                    if 0 <= a < n and 0 <= b < m and g[a][b] != -1:
                        d[i][j] = min(d[i][j], d[a][b] + 1)
    for i in range(n):
        for j in range(m):
            if g[i][j] == 2: return d[i][j] if d[i][j] < INF else -1

assert shortestRescue(4,4,[[1,-1,-1,-1],[0,0,0,0],[0,0,-1,0],[0,0,-1,2]]) == 7
assert shortestRescue(5,5,[[1,-1,-1,-1,-1],[0,-1,-1,-1,-1],[0,-1,0,0,0],[0,-1,0,-1,0],[0,0,0,-1,2]]) == 13
for _ in range(300):
    n, m = random.randint(2,6), random.randint(2,6)
    g = [[random.choice([0,0,-1]) for _ in range(m)] for _ in range(n)]
    cells = [(i,j) for i in range(n) for j in range(m)]
    s, t = random.sample(cells, 2)
    g[s[0]][s[1]] = 1; g[t[0]][t[1]] = 2
    assert shortestRescue(n,m,g) == brute(n,m,g)
print('ok')

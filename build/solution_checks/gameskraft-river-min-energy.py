from collections import deque


def minimum_energy(river, sx, sy, fx, fy):
    n, m = len(river), len(river[0])
    INF = float('inf')
    dist = [[INF] * m for _ in range(n)]
    dist[sx][sy] = 0
    dq = deque([(sx, sy)])
    # moves: (dx, dy, cost): right/down are free, left/up cost 1
    moves = ((0, 1, 0), (1, 0, 0), (0, -1, 1), (-1, 0, 1))
    while dq:
        x, y = dq.popleft()
        d = dist[x][y]
        for dx, dy, c in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and river[nx][ny] != '#' and d + c < dist[nx][ny]:
                dist[nx][ny] = d + c
                if c == 0:
                    dq.appendleft((nx, ny))          # 0-1 BFS: free edges to the front
                else:
                    dq.append((nx, ny))
    return -1 if dist[fx][fy] == INF else dist[fx][fy]

# ---- tests
import heapq, random
g = ["....." , "...#.", "..#.#", "....."]
assert minimum_energy(g, 2, 3, 1, 4) == 5
assert minimum_energy([".#.", ".##", "..."], 2, 0, 0, 2) == -1
def dijkstra(river, sx, sy, fx, fy):
    n, m = len(river), len(river[0]); dist = {(sx, sy): 0}; pq = [(0, sx, sy)]
    while pq:
        d, x, y = heapq.heappop(pq)
        if d > dist.get((x, y), 10**9): continue
        for dx, dy, c in ((0,1,0),(1,0,0),(0,-1,1),(-1,0,1)):
            nx, ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<m and river[nx][ny] != '#' and d+c < dist.get((nx,ny), 10**9):
                dist[(nx,ny)] = d+c; heapq.heappush(pq, (d+c, nx, ny))
    return dist.get((fx, fy), -1)
for _ in range(300):
    n, m = random.randint(1, 6), random.randint(1, 6)
    river = [''.join('#' if random.random() < .3 else '.' for _ in range(m)) for _ in range(n)]
    cells = [(i, j) for i in range(n) for j in range(m) if river[i][j] == '.']
    if not cells: continue
    s, f = random.choice(cells), random.choice(cells)
    assert minimum_energy(river, *s, *f) == dijkstra(river, *s, *f)
print('ok')

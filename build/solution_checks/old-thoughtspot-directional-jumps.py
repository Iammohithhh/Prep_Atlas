from collections import deque


def min_jumps(grid):
    R, C = len(grid), len(grid[0])
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                s = (r, c)
            elif grid[r][c] == 'E':
                e = (r, c)
    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    FREE = 4                                   # state: 4 = free, 0..3 = forced direction
    dist = {(s[0], s[1], FREE): 0}
    q = deque([(s[0], s[1], FREE)])
    while q:
        r, c, st = q.popleft()
        d = dist[(r, c, st)]
        if (r, c) == e and st == FREE:
            return d
        for di in ([st] if st != FREE else range(4)):
            dr, dc = DIRS[di]
            k = 1
            while True:
                nr, nc = r + dr * k, c + dc * k
                if not (0 <= nr < R and 0 <= nc < C):
                    break
                if grid[nr][nc] != '#':
                    nst = FREE if k == 1 else di
                    if (nr, nc, nst) not in dist:
                        dist[(nr, nc, nst)] = d + 1
                        q.append((nr, nc, nst))
                k += 1
    return -1

# ---- tests
import random
g = ["S****#", "**#***", "*****#", "*#*#**", "#****E"]
assert min_jumps(g) == 5
assert min_jumps(["SE"]) == 1
def brute(grid):
    R, C = len(grid), len(grid[0])
    pos = {grid[r][c]: (r, c) for r in range(R) for c in range(C) if grid[r][c] in 'SE'}
    layer = {(pos['S'][0], pos['S'][1], None)}
    seen = set(layer)
    for steps in range(0, R * C * 5 + 2):
        for (r, c, forced) in layer:
            if (r, c) == pos['E'] and forced is None:
                return steps
        nxt = set()
        for (r, c, forced) in layer:
            for dr, dc in ([forced] if forced else [(-1, 0), (1, 0), (0, -1), (0, 1)]):
                for k in range(1, max(R, C)):
                    nr, nc = r + dr * k, c + dc * k
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != '#':
                        st = (nr, nc, None if k == 1 else (dr, dc))
                        if st not in seen:
                            seen.add(st); nxt.add(st)
        if not nxt:
            return -1
        layer = nxt
    return -1
for _ in range(300):
    R, C = random.randint(1, 4), random.randint(2, 5)
    cells = [random.choice('**#') for _ in range(R * C)]
    a, b = random.sample(range(R * C), 2)
    cells[a] = 'S'; cells[b] = 'E'
    grid = [''.join(cells[i * C:(i + 1) * C]) for i in range(R)]
    assert min_jumps(grid) == brute(grid), grid
print('ok')

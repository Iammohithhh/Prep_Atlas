from collections import deque


def solution(forth):
    x = y = 0
    xs = [0]
    for ch in forth:
        if ch == 'N': y += 1
        elif ch == 'E': x += 1
        else: x -= 1
        xs.append(x)
    X, H = x, y
    best = None
    for col in (min(xs) - 1, max(xs) + 1):
        length = abs(X - col) + H + abs(col)
        if best is None or length < best[0]:
            best = (length, col)
    col = best[1]
    path = ''
    path += ('E' if col > X else 'W') * abs(col - X)
    path += 'S' * H
    path += ('E' if 0 > col else 'W') * abs(col)
    return path

# ---- tests
import random
assert solution("NEENWN") == "WWSSSE"
def walk(forth):
    pos = (0, 0); cells = [pos]
    for ch in forth:
        pos = (pos[0] + (ch == 'E') - (ch == 'W'), pos[1] + (ch == 'N'))
        cells.append(pos)
    return cells
def brute_len(forth):
    cells = walk(forth)
    used = set(cells)
    start, goal = cells[-1], (0, 0)
    blocked = used - {start, goal}
    used_edges = {frozenset((cells[i], cells[i + 1])) for i in range(len(cells) - 1)}
    dist = {start: 0}; dq = deque([start])
    while dq:
        p = dq.popleft()
        if p == goal: return dist[p]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (p[0] + dx, p[1] + dy)
            if abs(q[0]) > 12 or abs(q[1]) > 12 or q in blocked or q in dist: continue
            if frozenset((p, q)) in used_edges: continue
            dist[q] = dist[p] + 1; dq.append(q)
    return None
def valid(forth, back):
    cells = walk(forth); used = set(cells)
    pos = cells[-1]; goal = (0, 0)
    used_edges = {frozenset((cells[i], cells[i + 1])) for i in range(len(cells) - 1)}
    for ch in back:
        nxt = (pos[0] + (ch == 'E') - (ch == 'W'), pos[1] + (ch == 'N') - (ch == 'S'))
        if frozenset((pos, nxt)) in used_edges: return False
        if nxt in used and nxt != goal: return False
        pos = nxt
    return pos == goal
for _ in range(400):
    L = random.randint(2, 8)
    s = ['N']
    cx = 0; cy = 1; vis = {(0, 0), (0, 1)}
    for _ in range(L - 2):
        ch = random.choice('NEW')
        nx, ny = cx + (ch == 'E') - (ch == 'W'), cy + (ch == 'N')
        if (nx, ny) in vis: continue
        s.append(ch); vis.add((nx, ny)); cx, cy = nx, ny
    nx, ny = cx, cy + 1
    if (nx, ny) in vis: continue
    s.append('N'); forth = ''.join(s)
    back = solution(forth)
    assert valid(forth, back), (forth, back)
    assert len(back) == brute_len(forth), (forth, back, brute_len(forth))
print('ok')

def num_islands(grid):
    if not grid:
        return 0
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '1' and not seen[r][c]:
                count += 1
                seen[r][c] = True
                stack = [(r, c)]
                while stack:
                    x, y = stack.pop()
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= nx < R and 0 <= ny < C and grid[nx][ny] == '1' and not seen[nx][ny]:
                            seen[nx][ny] = True
                            stack.append((nx, ny))
    return count

# ---- tests
import random
assert num_islands(["11110", "11010", "11000", "00000"]) == 1
assert num_islands(["11000", "11000", "00100", "00011"]) == 3
assert num_islands([]) == 0
def brute(grid):
    R, C = len(grid), len(grid[0])
    parent = {(r, c): (r, c) for r in range(R) for c in range(C) if grid[r][c] == '1'}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for (r, c) in list(parent):
        for nb in ((r + 1, c), (r, c + 1)):
            if nb in parent:
                parent[find((r, c))] = find(nb)
    return len({find(a) for a in parent})
for _ in range(300):
    R, C = random.randint(1, 6), random.randint(1, 6)
    g = [''.join(random.choice('01') for _ in range(C)) for _ in range(R)]
    assert num_islands(g) == brute(g)
print('ok')

from collections import deque
import random

def foodDistribution(input1, input2, input3):
    n, m, g = input1, input2, [row[:] for row in input3]
    parts = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] == 0:
                parts += 1
                g[i][j] = 1                  # mark visited
                q = deque([(i, j)])
                while q:
                    x, y = q.popleft()
                    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        a, b = x + dx, y + dy
                        if 0 <= a < n and 0 <= b < m and g[a][b] == 0:
                            g[a][b] = 1
                            q.append((a, b))
    return parts

def brute(n, m, g):
    seen = set(); c = 0
    def dfs(x, y):
        st = [(x, y)]
        while st:
            p = st.pop()
            if p in seen: continue
            seen.add(p)
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                a, b = p[0]+dx, p[1]+dy
                if 0 <= a < n and 0 <= b < m and g[a][b] == 0 and (a, b) not in seen:
                    st.append((a, b))
    for i in range(n):
        for j in range(m):
            if g[i][j] == 0 and (i, j) not in seen:
                c += 1; dfs(i, j)
    return c

assert foodDistribution(5,5,[[0,1,1,1,1],[0,0,1,0,1],[1,0,1,0,1],[1,1,0,1,1],[0,1,1,0,1]]) == 5
assert foodDistribution(3,5,[[0,1,0,1,0],[0,1,0,1,0],[0,0,0,1,1]]) == 2
for _ in range(300):
    n, m = random.randint(1,6), random.randint(1,6)
    g = [[random.randint(0,1) for _ in range(m)] for _ in range(n)]
    assert foodDistribution(n,m,g) == brute(n,m,g)
print('ok')

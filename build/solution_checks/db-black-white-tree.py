import random
from collections import defaultdict

def solve(N, color, edges):
    adj = [[] for _ in range(N + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent = [0] * (N + 1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:                                  # iterative DFS, root = 1
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)
    white = [0] * (N + 1)
    black = [0] * (N + 1)
    for u in reversed(order):                     # children before parents
        if color[u - 1] == '0':
            white[u] += 1
        else:
            black[u] += 1
        if parent[u] > 0:
            white[parent[u]] += white[u]
            black[parent[u]] += black[u]
    return [white[u] * black[u] for u in range(1, N + 1)]

def brute(N, color, edges):
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    par = {1: 0}
    st = [1]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in par:
                par[v] = u
                st.append(v)
    def sub(u):
        res = [u]
        for v in adj[u]:
            if par[v] == u:
                res += sub(v)
        return res
    out = []
    for u in range(1, N + 1):
        s = sub(u)
        out.append(sum(1 for i in range(len(s)) for j in range(i + 1, len(s)) if color[s[i] - 1] != color[s[j] - 1]))
    return out

assert solve(5, '11110', [[3, 1], [4, 3], [5, 3], [2, 4]]) == [4, 0, 3, 0, 0]
for _ in range(300):
    n = random.randint(1, 9)
    edges = [[i, random.randint(1, i - 1)] for i in range(2, n + 1)]
    col = ''.join(random.choice('01') for _ in range(n))
    assert solve(n, col, edges) == brute(n, col, edges)
print('ok')

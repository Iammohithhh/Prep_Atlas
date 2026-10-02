import random

def primeQuery(n, first, second, values, queries):
    top = max(values) + 2
    sieve = [True] * top
    sieve[0] = sieve[1] = False
    for i in range(2, int(top ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, top, i):
                sieve[j] = False
    adj = [[] for _ in range(n + 1)]
    for a, b in zip(first, second):
        adj[a].append(b)
        adj[b].append(a)
    parent = [0] * (n + 1)
    parent[1] = -1
    order, st = [], [1]
    while st:
        u = st.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                st.append(v)
    cnt = [0] * (n + 1)
    for u in reversed(order):
        if sieve[values[u - 1]]:
            cnt[u] += 1
        if parent[u] > 0:
            cnt[parent[u]] += cnt[u]
    return [cnt[q] for q in queries]

def brute(n, first, second, values, queries):
    adj = {i: [] for i in range(1, n + 1)}
    for a, b in zip(first, second):
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
    def isp(x):
        return x > 1 and all(x % d for d in range(2, int(x ** 0.5) + 1))
    def sub(u):
        res = [u]
        for v in adj[u]:
            if par[v] == u:
                res += sub(v)
        return res
    return [sum(1 for x in sub(q) if isp(values[x - 1])) for q in queries]

for _ in range(300):
    n = random.randint(1, 9)
    first = list(range(2, n + 1))
    second = [random.randint(1, i - 1) for i in first]
    vals = [random.randint(1, 30) for _ in range(n)]
    qs = [random.randint(1, n) for _ in range(4)]
    assert primeQuery(n, first, second, vals, qs) == brute(n, first, second, vals, qs)
print('ok')

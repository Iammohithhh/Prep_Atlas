import random

MOD = (1 << 61) - 1


def find_palindromes(n, edges, chars, queries):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    parent = [0] * (n + 1)
    children = [[] for _ in range(n + 1)]
    order = []
    stack = [1]
    seen = [False] * (n + 1)
    seen[1] = True
    while stack:
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if not seen[w]:
                seen[w] = True
                parent[w] = u
                children[u].append(w)
                stack.append(w)
    for u in range(1, n + 1):
        children[u].sort()                          # visit children in increasing node number
    size = [1] * (n + 1)
    for u in reversed(order):
        if parent[u]:
            size[parent[u]] += size[u]
    # iterative post-order: the global string P and, for each node, the end position of its block
    P = []
    end = [0] * (n + 1)
    st = [(1, 0)]
    while st:
        u, i = st.pop()
        if i < len(children[u]):
            st.append((u, i + 1))
            st.append((children[u][i], 0))
        else:
            P.append(chars[u - 1])
            end[u] = len(P)                         # block of u is P[end - size : end]
    base = random.randrange(10**6, MOD - 1)
    vals = [ord(c) for c in P]
    fwd = [0] * (n + 1)
    pw = [1] * (n + 1)
    for i in range(n):
        fwd[i + 1] = (fwd[i] * base + vals[i]) % MOD
        pw[i + 1] = pw[i] * base % MOD
    rev = [0] * (n + 1)                              # hash of reversed(P) prefixes
    for i in range(n):
        rev[i + 1] = (rev[i] * base + vals[n - 1 - i]) % MOD

    def get(h, l, r):                                # hash of positions [l, r)
        return (h[r] - h[l] * pw[r - l]) % MOD

    out = []
    for u in queries:
        r = end[u]
        l = r - size[u]
        # reversed block corresponds to positions [n - r, n - l) of reversed(P)
        out.append(1 if get(fwd, l, r) == get(rev, n - r, n - l) else 0)
    return out

# ---- tests
assert find_palindromes(5, [(1, 2), (1, 3), (2, 4), (2, 5)], "ababc", [1, 2]) == [0, 1]
def brute(n, edges, chars, queries):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    def make(u, p):
        s = ''
        for v in sorted(adj[u]):
            if v != p: s += make(v, u)
        return s + chars[u - 1]
    return [1 if make(u, 0 if u == 1 else None) == make(u, 0 if u == 1 else None)[::-1] else 0 for u in queries]
def brute2(n, edges, chars, queries):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    par = {1: 0}; order = [1]
    for u in order:
        for w in adj[u]:
            if w not in par: par[w] = u; order.append(w)
    kids = {u: sorted(w for w in adj[u] if par.get(w) == u) for u in range(1, n + 1)}
    def make(u): return ''.join(make(v) for v in kids[u]) + chars[u - 1]
    return [1 if make(u) == make(u)[::-1] else 0 for u in queries]
for _ in range(300):
    n = random.randint(1, 10)
    edges = [(random.randint(1, i), i + 1) for i in range(1, n)]
    chars = ''.join(random.choice('ab') for _ in range(n))
    qs = list(range(1, n + 1))
    assert find_palindromes(n, edges, chars, qs) == brute2(n, edges, chars, qs)
find_palindromes(200000, [(i, i + 1) for i in range(1, 200000)], 'a' * 200000, [1, 100000])
print('ok')

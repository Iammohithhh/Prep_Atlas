from collections import defaultdict


def count_good_edge(n, k, values, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    parent = [0] * (n + 1)
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
                stack.append(w)
    size = [1] * (n + 1)
    for u in reversed(order):
        if parent[u]:
            size[parent[u]] += size[u]
    children = [[] for _ in range(n + 1)]
    for u in order:
        if parent[u]:
            children[parent[u]].append(u)
    tin = [0] * (n + 1)
    nodes = []                                  # Euler order: subtree of u = nodes[tin[u] : tin[u] + size[u]]
    stack = [1]
    while stack:
        u = stack.pop()
        tin[u] = len(nodes)
        nodes.append(u)
        for c in children[u]:
            stack.append(c)
    heavy = [0] * (n + 1)
    for u in range(1, n + 1):
        heavy[u] = max(children[u], key=lambda c: size[c], default=0)
    total = defaultdict(int)
    for v in values:
        total[v] += 1

    cnt = defaultdict(int)
    # over  = number of values whose count in the current set exceeds k
    # under = number of values with total > k whose count is below total - k (the rest of the tree would exceed k)
    state = {'over': 0, 'under': sum(1 for v in total if total[v] > k)}

    def flags(v):
        c = cnt[v]
        return (1 if c > k else 0), (1 if total[v] > k and c < total[v] - k else 0)

    def add(x, d):
        v = values[x - 1]
        o0, u0 = flags(v)
        cnt[v] += d
        o1, u1 = flags(v)
        state['over'] += o1 - o0
        state['under'] += u1 - u0

    good = 0
    # iterative DSU-on-tree (sack). A frame is (node, phase, keep).
    st = [(1, 0, True)]
    while st:
        u, phase, keep = st.pop()
        if phase == 0:
            st.append((u, 1, keep))
            if heavy[u]:
                st.append((heavy[u], 0, True))      # popped after all light children
            for c in children[u]:
                if c != heavy[u]:
                    st.append((c, 0, False))        # popped first; each one clears itself afterwards
        else:
            add(u, 1)
            for c in children[u]:
                if c != heavy[u]:
                    for x in nodes[tin[c]:tin[c] + size[c]]:
                        add(x, 1)
            if u != 1 and state['over'] == 0 and state['under'] == 0:
                good += 1                           # the edge (parent[u], u) is good
            if not keep:
                for x in nodes[tin[u]:tin[u] + size[u]]:
                    add(x, -1)
    return good

# ---- tests
import random
assert count_good_edge(5, 3, [1, 1, 1, 2, 1], [(1, 2), (1, 3), (2, 4), (3, 5)]) == 3
assert count_good_edge(4, 2, [1, 1, 1, 1], [(1, 2), (1, 3), (1, 4)]) == 0
def brute(n, k, values, edges):
    good = 0
    for i, (a, b) in enumerate(edges):
        adj = [[] for _ in range(n + 1)]
        for j, (u, v) in enumerate(edges):
            if j != i: adj[u].append(v); adj[v].append(u)
        seen = {a}; st = [a]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen: seen.add(w); st.append(w)
        side1 = defaultdict(int); side2 = defaultdict(int)
        for x in range(1, n + 1):
            (side1 if x in seen else side2)[values[x - 1]] += 1
        if max(side1.values(), default=0) <= k and max(side2.values(), default=0) <= k: good += 1
    return good
for _ in range(500):
    n = random.randint(2, 12); k = random.randint(1, n)
    values = [random.randint(1, 3) for _ in range(n)]
    edges = [(random.randint(1, i), i + 1) for i in range(1, n)]
    assert count_good_edge(n, k, values, edges) == brute(n, k, values, edges), (n, k, values, edges)
n = 100000
count_good_edge(n, 5, [random.randint(1, 50) for _ in range(n)], [(i, i + 1) for i in range(1, n)])
count_good_edge(n, 5, [random.randint(1, 50) for _ in range(n)], [(random.randint(1, i), i + 1) for i in range(1, n)])
print('ok')

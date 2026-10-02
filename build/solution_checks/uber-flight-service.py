import sys
sys.setrecursionlimit(1 << 16)
NEG = -10**9


def flight_sum(n, s, a):
    """s[i] in 'OR' (country i+1); a[i] (1-based) connects country i+2 with country a[i]."""
    adj = [[] for _ in range(n)]
    for i, p in enumerate(a):
        adj[i + 1].append(p - 1)
        adj[p - 1].append(i + 1)
    r_total = s.count('R')
    k = r_total - (r_total % 2)           # permissions come in pairs and cannot exceed |R|

    def best_from(root):
        # f[v][j] = max countries in a connected piece containing v, inside v's subtree, using j conversions
        order, parent = [], [-1] * n
        stack = [root]
        seen = [False] * n
        seen[root] = True
        while stack:
            u = stack.pop()
            order.append(u)
            for w in adj[u]:
                if not seen[w]:
                    seen[w] = True
                    parent[w] = u
                    stack.append(w)
        f = [None] * n
        for v in reversed(order):
            cost = 1 if s[v] == 'R' else 0
            cur = [NEG] * (k + 1)
            if cost <= k:
                cur[cost] = 1
            for w in adj[v]:
                if w == parent[v]:
                    continue
                child = f[w]
                new = cur[:]                       # option: do not extend into w
                for j in range(k + 1):
                    if cur[j] < 0:
                        continue
                    for t in range(k + 1 - j):
                        if child[t] >= 0 and cur[j] + child[t] > new[j + t]:
                            new[j + t] = cur[j] + child[t]
                cur = new
            f[v] = cur
        return max(f[root])                        # at most k conversions; unused ones go to unreachable R's

    return sum(max(best_from(v), 0) for v in range(n))

# ---- tests
import random
from itertools import combinations
assert flight_sum(7, "ROROROO", [1, 1, 3, 3, 5, 5]) == 33
def brute(n, s, a):
    adj = [[] for _ in range(n)]
    for i, p in enumerate(a):
        adj[i + 1].append(p - 1); adj[p - 1].append(i + 1)
    rs = [i for i in range(n) if s[i] == 'R']
    k = len(rs) - len(rs) % 2
    total = 0
    for v in range(n):
        best = 0
        for c in range(0, k + 1, 2):
            for conv in combinations(rs, c):
                open_ = {i for i in range(n) if s[i] == 'O'} | set(conv)
                if v not in open_: continue
                seen = {v}; st = [v]
                while st:
                    u = st.pop()
                    for w in adj[u]:
                        if w in open_ and w not in seen: seen.add(w); st.append(w)
                best = max(best, len(seen))
        total += best
    return total
for _ in range(300):
    n = random.randint(1, 9)
    s = ''.join(random.choice('OR') for _ in range(n))
    a = [random.randint(1, i) for i in range(1, n)]   # random tree: country i+1 attaches to an earlier one
    assert flight_sum(n, s, a) == brute(n, s, a), (n, s, a)
print('ok')

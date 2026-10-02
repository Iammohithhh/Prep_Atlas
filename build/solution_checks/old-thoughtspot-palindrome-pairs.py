from collections import defaultdict


def num_nice_pairs(n, g_from, g_to, g_weight):
    adj = [[] for _ in range(n + 1)]
    for a, b, w in zip(g_from, g_to, g_weight):
        adj[a].append((b, w))
        adj[b].append((a, w))
    mask = [0] * (n + 1)
    seen = [False] * (n + 1)
    seen[1] = True
    order = [1]
    for u in order:                            # BFS order, no recursion
        for v, w in adj[u]:
            if not seen[v]:
                seen[v] = True
                mask[v] = mask[u] ^ (1 << (w - 1))
                order.append(v)
    freq = defaultdict(int)
    pairs = 0
    for u in order:
        m = mask[u]
        pairs += freq[m]
        for b in range(26):
            pairs += freq[m ^ (1 << b)]
        freq[m] += 1
    return pairs

# ---- tests
import random
assert num_nice_pairs(5, [1, 2, 3, 3], [2, 3, 4, 5], [2, 1, 1, 1]) == 9
def brute(n, fr, to, wt):
    adj = [[] for _ in range(n + 1)]
    for a, b, w in zip(fr, to, wt):
        adj[a].append((b, w)); adj[b].append((a, w))
    total = 0
    for s in range(1, n + 1):
        stack = [(s, 0, 0)]
        while stack:
            u, p, m = stack.pop()
            if u > s and bin(m).count('1') <= 1:
                total += 1
            for v, w in adj[u]:
                if v != p:
                    stack.append((v, u, m ^ (1 << (w - 1))))
    return total
for _ in range(300):
    n = random.randint(1, 10)
    fr = [random.randint(1, i) for i in range(1, n)]
    to = list(range(2, n + 1))
    wt = [random.randint(1, 4) for _ in range(n - 1)]
    assert num_nice_pairs(n, fr, to, wt) == brute(n, fr, to, wt)
print('ok')

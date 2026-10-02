def solution(A, B, N):
    adj = [[] for _ in range(N + 1)]
    for a, b in zip(A, B):
        adj[a].append((b, 1))                       # walking a -> b (away from 0) follows the road, so the road points the wrong way
        adj[b].append((a, 0))                       # walking b -> a goes against the road: it already points towards 0
    seen = [False] * (N + 1)
    seen[0] = True
    stack = [0]
    reversals = 0
    while stack:
        u = stack.pop()
        for v, c in adj[u]:
            if not seen[v]:
                seen[v] = True
                reversals += c                      # the edge must point from v to u (towards 0)
                stack.append(v)
    return reversals

# ---- tests
import random
assert solution([1, 2, 3], [0, 0, 1], 3) == 0
assert solution([0, 0, 1], [1, 2, 3], 3) == 3
def brute(A, B, N):
    best = N + 1
    for mask in range(1 << N):
        edges = [(B[i], A[i]) if mask >> i & 1 else (A[i], B[i]) for i in range(N)]
        ok = True
        for s in range(1, N + 1):
            cur = {s}; ch = True
            while ch:
                ch = False
                for u, v in edges:
                    if u in cur and v not in cur: cur.add(v); ch = True
            if 0 not in cur: ok = False; break
        if ok: best = min(best, bin(mask).count('1'))
    return best
for _ in range(300):
    N = random.randint(1, 8)
    A, B = [], []
    for v in range(1, N + 1):
        p = random.randint(0, v - 1)
        if random.random() < .5: A.append(v); B.append(p)
        else: A.append(p); B.append(v)
    assert solution(A, B, N) == brute(A, B, N), (A, B)
print('ok')

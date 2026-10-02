from itertools import combinations


def count_min_selections(n, c, v):
    """Number of minimum-size sets of houses such that every window of c consecutive houses has >= v chosen.
    DP over positions keeping the last c-1 choices; returns (min size, number of ways) modulo 10^9+7 for the count."""
    MOD = 10**9 + 7
    INF = float('inf')
    w = c - 1
    full = (1 << w) - 1
    # state: bitmask of the last min(i, w) choices (most recent in bit 0)
    cur = {0: (0, 1)}
    for i in range(n):
        nxt = {}
        for mask, (cost, ways) in cur.items():
            for take in (0, 1):
                if i + 1 >= c:                       # a full window ends at position i
                    if bin(mask).count('1') + take < v:
                        continue
                nm = ((mask << 1) | take) & full if w > 0 else 0
                nc = cost + take
                if nm not in nxt or nc < nxt[nm][0]:
                    nxt[nm] = (nc, ways % MOD)
                elif nc == nxt[nm][0]:
                    nxt[nm] = (nc, (nxt[nm][1] + ways) % MOD)
        cur = nxt
    best = min(cost for cost, _ in cur.values())
    return best, sum(w_ for cost, w_ in cur.values() if cost == best) % MOD

# ---- tests
import random
assert count_min_selections(4, 2, 1)[1] == 3
def brute(n, c, v):
    best = None; cnt = 0
    for mask in range(1 << n):
        sel = [i for i in range(n) if mask >> i & 1]
        ok = all(sum(1 for i in range(s, s + c) if mask >> i & 1) >= v for s in range(0, n - c + 1))
        if ok:
            k = len(sel)
            if best is None or k < best: best, cnt = k, 1
            elif k == best: cnt += 1
    return best, cnt
for _ in range(200):
    n = random.randint(1, 10); c = random.randint(1, n); v = random.randint(1, c)
    assert count_min_selections(n, c, v) == brute(n, c, v), (n, c, v)
print('ok')

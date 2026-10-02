def max_players(n, m, ratings):
    p = sorted(ratings)
    # reach[i] = first index j such that p[j] - p[i] > 5, so window [i, reach[i]) is a valid team
    reach = [0] * n
    j = 0
    for i in range(n):
        while j < n and p[j] - p[i] <= 5:
            j += 1
        reach[i] = j
    # prev[i] = best total using the first i sorted players with at most t teams
    prev = [0] * (n + 1)
    for _ in range(m):
        cur = prev[:]
        for i in range(n):
            if cur[i] > cur[i + 1]:          # skip player i
                cur[i + 1] = cur[i]
            val = prev[i] + reach[i] - i     # open a team at i and take p[i..reach[i]-1]
            if val > cur[reach[i]]:
                cur[reach[i]] = val
        for i in range(n):                    # propagate prefix maxima
            if cur[i] > cur[i + 1]:
                cur[i + 1] = cur[i]
        prev = cur
    return prev[n]

# ---- tests
import random
from itertools import product
assert max_players(6, 2, [33, 5, 8, 20, 17, 3]) == 5
def brute(n, m, r):
    best = 0
    for asg in product(range(m + 1), repeat=n):   # 0 = not picked
        ok = True
        for t in range(1, m + 1):
            grp = [r[i] for i in range(n) if asg[i] == t]
            if grp and max(grp) - min(grp) > 5: ok = False; break
        if ok: best = max(best, sum(1 for a in asg if a))
    return best
for _ in range(150):
    n = random.randint(1, 6); m = random.randint(1, min(3, n))
    r = [random.randint(1, 20) for _ in range(n)]
    assert max_players(n, m, r) == brute(n, m, r), (n, m, r)
print('ok')

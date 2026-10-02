def max_effort(n, s):
    full = (1 << n) - 1
    # gain[mask] = sum of s[i][j] over pairs i<j inside mask
    gain = [0] * (1 << n)
    for mask in range(1, 1 << n):
        low = (mask & -mask).bit_length() - 1
        rest = mask & (mask - 1)
        g = gain[rest]
        m = rest
        while m:
            j = (m & -m).bit_length() - 1
            g += s[low][j]
            m &= m - 1
        gain[mask] = g
    NEG = float('-inf')
    dp = [NEG] * (1 << n)
    dp[0] = 0
    for mask in range(1, 1 << n):
        low = mask & -mask               # the lowest driver must be in some team
        rest = mask ^ low
        sub = rest
        best = NEG
        while True:
            team = sub | low
            v = gain[team] + dp[mask ^ team]
            if v > best:
                best = v
            if sub == 0:
                break
            sub = (sub - 1) & rest
        dp[mask] = best
    return dp[full]

# ---- tests
import random
assert max_effort(3, [[0, 5, 8], [5, 0, -10], [8, -10, 0]]) == 8
assert max_effort(4, [[0, 10, 10, 10], [10, 0, 10, 10], [10, 10, 0, -1], [10, 10, -1, 0]]) == 49
def brute(n, s):
    best = [float('-inf')]
    def go(i, teams):
        if i == n:
            tot = sum(s[a][b] for t in teams for x, a in enumerate(t) for b in t[x + 1:])
            best[0] = max(best[0], tot); return
        for t in teams:
            t.append(i); go(i + 1, teams); t.pop()
        teams.append([i]); go(i + 1, teams); teams.pop()
    go(0, [])
    return best[0]
for _ in range(100):
    n = random.randint(1, 6)
    s = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s[i][j] = s[j][i] = random.randint(-10, 10)
    assert max_effort(n, s) == brute(n, s)
print('ok')

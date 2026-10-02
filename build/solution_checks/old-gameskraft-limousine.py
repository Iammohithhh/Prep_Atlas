def collect_max(mat):
    n = len(mat)
    NEG = float('-inf')
    # dp[r1][r2] after t steps: both walkers have taken t steps (r1 + c1 = r2 + c2 = t)
    dp = [[NEG] * n for _ in range(n)]
    if mat[0][0] == -1:
        return 0
    dp[0][0] = mat[0][0]
    for t in range(1, 2 * n - 1):
        nd = [[NEG] * n for _ in range(n)]
        for r1 in range(max(0, t - n + 1), min(n - 1, t) + 1):
            c1 = t - r1
            if mat[r1][c1] == -1:
                continue
            for r2 in range(max(0, t - n + 1), min(n - 1, t) + 1):
                c2 = t - r2
                if mat[r2][c2] == -1:
                    continue
                best = NEG
                for p1 in (r1, r1 - 1):                # previous row of walker 1 (came from left or from above)
                    for p2 in (r2, r2 - 1):
                        if 0 <= p1 < n and 0 <= p2 < n and dp[p1][p2] > best:
                            best = dp[p1][p2]
                if best == NEG:
                    continue
                gain = mat[r1][c1] + (mat[r2][c2] if (r1, c1) != (r2, c2) else 0)
                nd[r1][r2] = best + gain
        dp = nd
    return max(0, dp[n - 1][n - 1]) if dp[n - 1][n - 1] != NEG else 0

# ---- tests
import random
assert collect_max([[0, 1, -1], [1, 0, -1], [1, 1, 1]]) == 5
assert collect_max([[0, 1, 1], [1, 0, 1], [1, 1, 1]]) == 7
assert collect_max([[0, -1], [-1, 0]]) == 0
def brute(mat):
    n = len(mat)
    def paths(r, c, tr, tc, dr, dc):
        if mat[r][c] == -1: return
        if (r, c) == (tr, tc):
            yield [(r, c)]; return
        for a, b in ((dr, 0), (0, dc)):
            nr, nc = r + a, c + b
            if 0 <= nr < n and 0 <= nc < n:
                for p in paths(nr, nc, tr, tc, dr, dc): yield [(r, c)] + p
    best = 0
    fw = list(paths(0, 0, n - 1, n - 1, 1, 1))
    bw = list(paths(n - 1, n - 1, 0, 0, -1, -1))
    for p in fw:
        for q in bw:
            cells = set(p) | set(q)
            best = max(best, sum(1 for (r, c) in cells if mat[r][c] == 1))
    return best
for _ in range(200):
    n = random.randint(1, 4)
    mat = [[random.choice([0, 0, 1, 1, -1]) for _ in range(n)] for _ in range(n)]
    mat[0][0] = 0 if mat[0][0] == -1 else mat[0][0]
    assert collect_max(mat) == brute(mat), mat
print('ok')

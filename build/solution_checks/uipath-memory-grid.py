import random
NEG = float('-inf')

def findMaxDataRetrieved(mem, k):
    n, m = len(mem), len(mem[0])
    best_above = [NEG] * m
    for i in range(n):
        cur = [None] * m
        best_here = [NEG] * m
        for j in range(m):
            dp = [NEG] * (k + 1)
            if i == 0 and j == 0:
                top = 0
            elif i > 0:
                top = best_above[j]
            else:
                top = NEG
            if top > NEG:
                dp[0] = top
                dp[1] = top + mem[i][j]
            if j > 0:
                left = cur[j - 1]
                for c in range(k + 1):
                    if left[c] > dp[c]:
                        dp[c] = left[c]                        # skip this cell
                    if c > 0 and left[c - 1] > NEG and left[c - 1] + mem[i][j] > dp[c]:
                        dp[c] = left[c - 1] + mem[i][j]        # read this cell
            cur[j] = dp
            best_here[j] = max(dp)
        best_above = best_here
    return int(best_above[m - 1])

def brute(mem, k):
    n, m = len(mem), len(mem[0])
    best = 0
    def rec(i, j, picked, total):
        nonlocal best
        for read in (0, 1):
            if read and picked >= k:
                continue
            t = total + (mem[i][j] if read else 0)
            p = picked + read
            if i == n - 1 and j == m - 1:
                best = max(best, t)
            if j + 1 < m:
                rec(i, j + 1, p, t)
            if i + 1 < n:
                rec(i + 1, j, 0, t)
    rec(0, 0, 0, 0)
    return best

assert findMaxDataRetrieved([[3, 4, 10], [2, 8, 1]], 2) == 16
assert findMaxDataRetrieved([[2, 3, 2, 4], [2, 4, 5, 1]], 2) == 14
for _ in range(300):
    n = random.randint(1, 3)
    m = random.randint(1, 4)
    k = random.randint(1, min(3, m))
    mem = [[random.randint(1, 9) for _ in range(m)] for _ in range(n)]
    assert findMaxDataRetrieved(mem, k) == brute(mem, k), (mem, k)
print('ok')

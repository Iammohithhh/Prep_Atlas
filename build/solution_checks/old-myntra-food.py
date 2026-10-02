def squirrel_food(n, k, positions):
    p = sorted(positions)
    pre = [0]
    for x in p:
        pre.append(pre[-1] + x)

    def cost(i, j):                                  # serve p[i..j] with one packet at the median
        mid = (i + j) // 2
        left = p[mid] * (mid - i + 1) - (pre[mid + 1] - pre[i])
        right = (pre[j + 1] - pre[mid + 1]) - p[mid] * (j - mid)
        return left + right

    INF = float('inf')
    dp = [[INF] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 0
    for g in range(1, k + 1):
        for j in range(1, n + 1):
            for i in range(g - 1, j):
                if dp[g - 1][i] + cost(i, j - 1) < dp[g][j]:
                    dp[g][j] = dp[g - 1][i] + cost(i, j - 1)
    return min(dp[g][n] for g in range(1, k + 1))

# ---- tests
import random
from itertools import combinations
assert squirrel_food(5, 2, [2, 3, 5, 12, 19]) == 10
assert squirrel_food(6, 2, [1, 2, 3, 4, 5, 100]) == 6
def brute(n, k, pos):
    lo, hi = min(pos), max(pos)
    best = 10**9
    for cs in combinations(range(lo, hi + 1), min(k, hi - lo + 1)):
        best = min(best, sum(min(abs(x - c) for c in cs) for x in pos))
    return best
for _ in range(300):
    n = random.randint(1, 7); k = random.randint(1, n); pos = [random.randint(1, 14) for _ in range(n)]
    assert squirrel_food(n, k, pos) == brute(n, k, pos), (n, k, pos)
print('ok')

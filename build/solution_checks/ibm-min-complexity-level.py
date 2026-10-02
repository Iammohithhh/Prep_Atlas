def find_min_complexity(complexity, days):
    n = len(complexity)
    INF = float('inf')
    # dp[d][i] = min total complexity to attend the first i lectures over exactly d days
    dp = [[INF] * (n + 1) for _ in range(days + 1)]
    dp[0][0] = 0
    for d in range(1, days + 1):
        for i in range(d, n + 1):
            day_max = 0
            for j in range(i - 1, d - 2, -1):          # last day covers lectures j..i-1
                day_max = max(day_max, complexity[j])
                if dp[d - 1][j] + day_max < dp[d][i]:
                    dp[d][i] = dp[d - 1][j] + day_max
    return dp[days][n]

# ---- tests
import random
assert find_min_complexity([30, 10, 40, 20, 50], 2) == 80
assert find_min_complexity([1, 5, 3, 2, 4], 2) == 6
def brute(c, days):
    n = len(c)
    from itertools import combinations
    best = float('inf')
    for cuts in combinations(range(1, n), days - 1):
        b = (0,) + cuts + (n,)
        best = min(best, sum(max(c[b[k]:b[k + 1]]) for k in range(days)))
    return best
for _ in range(300):
    n = random.randint(1, 8); d = random.randint(1, n); c = [random.randint(1, 20) for _ in range(n)]
    assert find_min_complexity(c, d) == brute(c, d)
print('ok')

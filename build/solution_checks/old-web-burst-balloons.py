def max_coins(nums):
    a = [1] + nums + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]          # dp[i][j]: best for balloons strictly between i and j
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):         # k is the LAST balloon to burst in (i, j)
                dp[i][j] = max(dp[i][j], dp[i][k] + a[i] * a[k] * a[j] + dp[k][j])
    return dp[0][n - 1]

# ---- tests
import random
from itertools import permutations
assert max_coins([3, 1, 5, 8]) == 167
assert max_coins([1, 5]) == 10
assert max_coins([]) == 0
def brute(nums):
    best = 0
    for order in permutations(range(len(nums))):
        alive = list(range(len(nums)))
        total = 0
        for idx in order:
            p = alive.index(idx)
            left = nums[alive[p - 1]] if p > 0 else 1
            right = nums[alive[p + 1]] if p + 1 < len(alive) else 1
            total += left * nums[idx] * right
            alive.pop(p)
        best = max(best, total)
    return best
for _ in range(200):
    nums = [random.randint(0, 6) for _ in range(random.randint(0, 6))]
    assert max_coins(nums) == brute(nums), nums
print('ok')

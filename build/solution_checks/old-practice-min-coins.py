def min_coins(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == INF else dp[amount]

# ---- tests
import random
from collections import deque
assert min_coins([1, 2, 5], 11) == 3
assert min_coins([2], 3) == -1
assert min_coins([5], 0) == 0
def brute(coins, amount):
    dist = {0: 0}
    q = deque([0])
    while q:
        x = q.popleft()
        for c in coins:
            y = x + c
            if y <= amount and y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    return dist.get(amount, -1)
for _ in range(400):
    coins = [random.randint(1, 9) for _ in range(random.randint(1, 4))]
    amount = random.randint(0, 30)
    assert min_coins(coins, amount) == brute(coins, amount)
print('ok')

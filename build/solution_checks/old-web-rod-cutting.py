def rod_cutting(prices, n):
    """prices[i] is the price of a piece of length i + 1."""
    best = [0] * (n + 1)
    for length in range(1, n + 1):
        for cut in range(1, min(length, len(prices)) + 1):
            best[length] = max(best[length], prices[cut - 1] + best[length - cut])
    return best[n]

# ---- tests
import random
from functools import lru_cache
assert rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 8) == 22
assert rod_cutting([3, 5, 8, 9, 10, 17, 17, 20], 8) == 24
assert rod_cutting([2], 0) == 0
def brute(prices, n):
    @lru_cache(None)
    def go(rem):
        if rem == 0:
            return 0
        return max(prices[c - 1] + go(rem - c) for c in range(1, min(rem, len(prices)) + 1))
    return go(n)
for _ in range(300):
    prices = [random.randint(1, 12) for _ in range(random.randint(1, 6))]
    n = random.randint(0, 9)
    assert rod_cutting(prices, n) == brute(tuple(prices), n)
print('ok')

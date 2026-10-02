def good_subarrays(n, arr, x):
    def at_least(y):
        """Number of subarrays containing at least y values that occur >= 3 times."""
        freq = {}
        heavy = 0
        left = 0
        total = 0
        for r in range(n):
            v = arr[r]
            freq[v] = freq.get(v, 0) + 1
            if freq[v] == 3:
                heavy += 1
            if heavy >= y:
                # shrink the left end while the window still has >= y heavy values
                while True:
                    f = freq[arr[left]]
                    after = heavy - (1 if f == 3 else 0)
                    if after < y:
                        break
                    freq[arr[left]] -= 1
                    heavy = after
                    left += 1
                total += left + 1                  # starts 0..left all give >= y heavy values
        return total
    return at_least(x) - at_least(x + 1)

# ---- tests
import random
assert good_subarrays(6, [1, 2, 2, 2, 1, 1], 2) == 1
assert good_subarrays(7, [1, 2, 2, 3, 3, 2, 3], 1) == 4
def brute(n, arr, x):
    c = 0
    for l in range(n):
        for r in range(l, n):
            sub = arr[l:r + 1]
            if sum(1 for v in set(sub) if sub.count(v) >= 3) == x: c += 1
    return c
for _ in range(500):
    n = random.randint(1, 14); arr = [random.randint(1, 3) for _ in range(n)]; x = random.randint(1, 3)
    assert good_subarrays(n, arr, x) == brute(n, arr, x), (arr, x)
print('ok')

def find_longest_subsequence(arr):
    a = sorted(arr)
    best = 0
    for p in (0, 1):
        idx = [i for i, v in enumerate(a) if v % 2 == p]
        if idx:
            best = max(best, idx[-1] - idx[0] + 1)
    return best

# ---- tests
import random
assert find_longest_subsequence([2, 4, 1, 7]) == 4
assert find_longest_subsequence([7, 5, 6, 2, 3, 2, 4]) == 6
def brute(arr):
    best = 0
    n = len(arr)
    for mask in range(1, 1 << n):
        s = sorted(arr[i] for i in range(n) if mask >> i & 1)
        if sum(s[i + 1] - s[i] for i in range(len(s) - 1)) % 2 == 0:
            best = max(best, len(s))
    return best
for _ in range(400):
    arr = [random.randint(0, 9) for _ in range(random.randint(1, 9))]
    assert find_longest_subsequence(arr) == brute(arr), arr
print('ok')

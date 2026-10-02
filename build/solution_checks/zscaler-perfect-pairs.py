def get_perfect_pairs_count(arr):
    a = sorted(abs(x) for x in arr)
    count = 0
    lo = 0
    for hi in range(len(a)):
        while a[lo] * 2 < a[hi]:           # need a[hi] <= 2 * a[lo]
            lo += 1
        count += hi - lo                   # partners a[lo..hi-1]
    return count

# ---- tests
import random
assert get_perfect_pairs_count([2, 5, -3]) == 2
assert get_perfect_pairs_count([-9, 6, -2, 1]) == 2
def brute(arr):
    c = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            x, y = arr[i], arr[j]
            if min(abs(x - y), abs(x + y)) <= min(abs(x), abs(y)) and max(abs(x - y), abs(x + y)) >= max(abs(x), abs(y)): c += 1
    return c
for _ in range(500):
    arr = [random.randint(-12, 12) for _ in range(random.randint(2, 12))]
    assert get_perfect_pairs_count(arr) == brute(arr), arr
print('ok')

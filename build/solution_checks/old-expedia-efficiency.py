def get_max_efficiency(arrival):
    a = sorted(arrival)
    best = None
    best_left = a[0] - 0                      # max of a[i] - i over i < j
    for j in range(1, len(a)):
        cand = (j + 1 - a[j]) + best_left
        if best is None or cand > best:
            best = cand
        best_left = max(best_left, a[j] - j)
    return best

# ---- tests
import random
assert get_max_efficiency([9, 1, 3, 5, 6]) == 1
def brute(arr):
    best = None
    vals = sorted(set(arr))
    for t1 in vals:
        for t2 in vals:
            if t2 < t1:
                continue
            cnt = sum(1 for x in arr if t1 <= x <= t2)
            if cnt >= 2:
                e = cnt - (t2 - t1)
                if best is None or e > best:
                    best = e
    return best
for _ in range(500):
    arr = [random.randint(1, 15) for _ in range(random.randint(2, 8))]
    assert get_max_efficiency(arr) == brute(arr), arr
print('ok')

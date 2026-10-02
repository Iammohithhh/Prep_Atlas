from collections import Counter


def get_outlier_value(arr):
    total = sum(arr)
    freq = Counter(arr)
    best = None
    for o in freq:                                   # candidate outlier value
        rest = total - o                              # = sum of the normal numbers + the sum entry = 2 * s
        if rest % 2:
            continue
        s = rest // 2                                 # value of the sum entry
        need = 2 if s == o else 1                     # the sum entry and the outlier use different indices
        if freq.get(s, 0) >= need and (best is None or o > best):
            best = o
    return best

# ---- tests
import random
assert get_outlier_value([4, 1, 3, 16, 2, 10]) == 16
assert get_outlier_value([2, 2, 4, 2]) == 2
def brute(arr):
    n = len(arr); best = None
    for s in range(n):
        for o in range(n):
            if s == o: continue
            if sum(arr[i] for i in range(n) if i not in (s, o)) == arr[s]:
                if best is None or arr[o] > best: best = arr[o]
    return best
for _ in range(500):
    n = random.randint(3, 7)
    normal = [random.randint(1, 9) for _ in range(n - 2)]
    arr = normal + [sum(normal), random.randint(1, 30)]
    random.shuffle(arr)
    assert get_outlier_value(arr) == brute(arr), arr
print('ok')

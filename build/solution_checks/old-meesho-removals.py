def get_maximum_removals(order, source, target):
    n = len(source)
    removed_at = [0] * n                              # removal step (1-based) of each source position
    for step, idx in enumerate(order, 1):
        removed_at[idx - 1] = step

    def ok(k):                                        # target still a subsequence after the first k removals?
        j = 0
        for i in range(n):
            if removed_at[i] > k and j < len(target) and source[i] == target[j]:
                j += 1
        return j == len(target)

    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo

# ---- tests
import random
assert get_maximum_removals([1, 4, 2, 3, 5], "hkbdi", "kd") == 1
assert get_maximum_removals([7, 1, 2, 5, 4, 3, 6], "abbabaa", "bb") == 3
for _ in range(300):
    n = random.randint(1, 9); s = ''.join(random.choice('ab') for _ in range(n))
    idx = random.sample(range(n), random.randint(1, n)); t = ''.join(s[i] for i in sorted(idx))
    order = list(range(1, n + 1)); random.shuffle(order)
    def sub(a, b):
        it = iter(a); return all(ch in it for ch in b)
    best = 0
    for k in range(n + 1):
        rem = set(order[:k])
        if sub(''.join(s[i] for i in range(n) if i + 1 not in rem), t): best = k
    assert get_maximum_removals(order, s, t) == best
print('ok')

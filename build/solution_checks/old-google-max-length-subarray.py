from bisect import bisect_left


def longest_subarray(n, x, y, a):
    vals = sorted(set(a))
    idx = {v: i + 1 for i, v in enumerate(vals)}
    m = len(vals)
    cnt = [0] * (m + 1)                            # Fenwick tree: counts per value rank
    sm = [0] * (m + 1)                             # Fenwick tree: sums per value rank
    LOG = 1
    while (1 << LOG) <= m:
        LOG += 1

    def update(i, c, s):
        while i <= m:
            cnt[i] += c
            sm[i] += s
            i += i & -i

    def top_y_sum(total_count, total_sum, y):
        """Sum of the y largest values currently in the window."""
        if y >= total_count:
            return total_sum
        k = total_count - y                        # number of smallest elements to exclude
        pos = 0
        rem = k
        taken = 0
        for b in range(LOG, -1, -1):
            nxt = pos + (1 << b)
            if nxt <= m and cnt[nxt] <= rem:
                pos = nxt
                rem -= cnt[nxt]
                taken += sm[nxt]
        # `rem` more elements have value vals[pos] (rank pos + 1)
        if rem:
            taken += rem * vals[pos]
        return total_sum - taken

    left = 0
    total = 0
    c = 0
    best = 0
    for right in range(n):
        update(idx[a[right]], 1, a[right])
        total += a[right]
        c += 1
        while left <= right and total - top_y_sum(c, total, y) > x:
            update(idx[a[left]], -1, -a[left])
            total -= a[left]
            c -= 1
            left += 1
        best = max(best, right - left + 1)
    return best

# ---- tests
import random
assert longest_subarray(4, 2, 1, [4, 2, 0, 1]) == 3
assert longest_subarray(6, 4, 2, [4, 2, 1, 3, 2, 5]) == 4
def brute(n, x, y, a):
    best = 0
    for l in range(n):
        for r in range(l, n):
            w = sorted(a[l:r + 1], reverse=True)
            if sum(w[y:]) <= x: best = max(best, r - l + 1)
    return best
for _ in range(500):
    n = random.randint(1, 9); a = [random.randint(0, 9) for _ in range(n)]
    x = random.randint(0, 15); y = random.randint(0, 4)
    assert longest_subarray(n, x, y, a) == brute(n, x, y, a), (n, x, y, a)
print('ok')

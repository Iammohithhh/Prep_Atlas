from bisect import bisect_left, bisect_right


def min_operations(k, locks):
    a = sorted(locks)
    n = len(a)
    prefix = [0]
    for x in a:
        prefix.append(prefix[-1] + x)
    half = k // 2

    def range_sum(lo, hi):                           # sum of a[lo:hi]
        return prefix[hi] - prefix[lo]

    def cost(t):
        # |l - t| <= half  -> distance |l - t|; otherwise the long way round: k - |l - t|
        left_near = bisect_left(a, t - half)         # a[left_near:i_t] are within `half` below t
        i_t = bisect_right(a, t)                     # a[:i_t] <= t
        right_far = bisect_right(a, t + half)        # a[i_t:right_far] are within `half` above t
        total = t * (i_t - left_near) - range_sum(left_near, i_t)
        total += range_sum(i_t, right_far) - t * (right_far - i_t)
        far_low = left_near                           # values below t - half wrap around upward
        total += (k - t) * far_low + range_sum(0, far_low)
        far_high = n - right_far                      # values above t + half wrap around downward
        total += far_high * (k + t) - range_sum(right_far, n)
        return total

    return min(cost(t) for t in set(a))

# ---- tests
import random
assert min_operations(100, [1, 2, 99]) == 3
def brute(k, locks):
    def d(x, y):
        z = abs(x - y)
        return min(z, k - z)
    return min(sum(d(x, t) for x in locks) for t in range(1, k + 1))
for _ in range(500):
    k = random.randint(2, 15); n = random.randint(1, 8)
    locks = [random.randint(1, k) for _ in range(n)]
    assert min_operations(k, locks) == brute(k, locks), (k, locks)
print('ok')

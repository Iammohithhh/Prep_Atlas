def count_balancing_elements(arr):
    n = len(arr)
    # even_pre[i], odd_pre[i]: sums of even / odd indexed elements among arr[:i]
    even_pre = [0] * (n + 1)
    odd_pre = [0] * (n + 1)
    for i, x in enumerate(arr):
        even_pre[i + 1] = even_pre[i] + (x if i % 2 == 0 else 0)
        odd_pre[i + 1] = odd_pre[i] + (x if i % 2 == 1 else 0)
    count = 0
    for i in range(n):
        # elements after i shift down by one, so their parity flips
        even_after = even_pre[i] + (odd_pre[n] - odd_pre[i + 1])
        odd_after = odd_pre[i] + (even_pre[n] - even_pre[i + 1])
        if even_after == odd_after:
            count += 1
    return count

# ---- tests
import random
assert count_balancing_elements([5, 5, 2, 5, 8]) == 2
for _ in range(500):
    a = [random.randint(1, 6) for _ in range(random.randint(1, 10))]
    exp = 0
    for i in range(len(a)):
        b = a[:i] + a[i + 1:]
        if sum(b[0::2]) == sum(b[1::2]): exp += 1
    assert count_balancing_elements(a) == exp
print('ok')

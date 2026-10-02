def min_sub_array_len(nums, target):
    best = len(nums) + 1
    left = 0
    window = 0
    for right, x in enumerate(nums):
        window += x
        while window >= target:
            best = min(best, right - left + 1)
            window -= nums[left]
            left += 1
    return 0 if best == len(nums) + 1 else best

# ---- tests
import random
assert min_sub_array_len([2, 3, 1, 2, 4, 3], 7) == 2
assert min_sub_array_len([1, 1, 1, 1, 1, 1, 1, 1], 11) == 0
assert min_sub_array_len([5], 5) == 1
for _ in range(300):
    a = [random.randint(1, 6) for _ in range(random.randint(1, 10))]; t = random.randint(1, 30)
    exp = min((j - i + 1 for i in range(len(a)) for j in range(i, len(a)) if sum(a[i:j + 1]) >= t), default=0)
    assert min_sub_array_len(a, t) == exp
print('ok')

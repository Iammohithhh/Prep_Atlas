def max_subset_sum(nums):
    best = {}                                       # LSB (0 or 1) -> largest value with that LSB
    for x in nums:
        bit = x & 1
        if bit not in best or x > best[bit]:
            best[bit] = x
    return sum(best.values())

# ---- tests
assert max_subset_sum([3, 5, 7, 9]) == 9
assert max_subset_sum([2, 5, 7, 3, 9, 11]) == 13
print('ok')

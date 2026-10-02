def level_sum(a, level):
    """Sum of the nodes on a 1-indexed level of the array-embedded almost complete binary tree."""
    lo = 1 << (level - 1)                    # first position (1-indexed) on this level
    hi = min((1 << level) - 1, len(a))       # last position on this level
    if lo > len(a):
        return 0
    return sum(a[lo - 1:hi])

# ---- tests
assert level_sum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1) == 1
assert level_sum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3) == 4 + 5 + 6 + 7
assert level_sum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4) == 8 + 9 + 10
assert level_sum([1, 2, 3], 5) == 0
print('ok')

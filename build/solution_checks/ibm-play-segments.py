def play_segments(coins):
    n = len(coins)
    total = sum(1 if c else -1 for c in coins)
    pre = 0
    for s in range(n + 1):                            # Player 1 plays the first s segments
        if pre > total - pre:
            return s
        if s < n:
            pre += 1 if coins[s] else -1
    return -1                                         # not possible (assumed not to occur)

# ---- tests
assert play_segments([1, 1, 0, 1]) == 2
assert play_segments([1, 0, 0, 1, 0]) == 0
assert play_segments([0, 0]) == 0
assert play_segments([1]) == 1
print('ok')

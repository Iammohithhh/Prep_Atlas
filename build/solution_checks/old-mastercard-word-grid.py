def count_word(grid, word):
    n = len(grid)
    m = len(word)
    total = 0
    for r in range(n):
        for c in range(n):
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    er, ec = r + dr * (m - 1), c + dc * (m - 1)
                    if not (0 <= er < n and 0 <= ec < n):
                        continue
                    if all(grid[r + dr * k][c + dc * k] == word[k] for k in range(m)):
                        total += 1
    return total

# ---- tests
assert count_word(["ctt", "cat", "cct"], "cat") == 4
assert count_word(["aaa", "aaa", "aaa"], "a") == 9 * 8
print('ok')

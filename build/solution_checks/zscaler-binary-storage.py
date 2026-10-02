def sort_binary_numbers(bit_arrays):
    n = len(bit_arrays)
    # all rows have the same number of set bits, so comparing the bit indices from the highest down
    # lexicographically is the same as comparing the numbers
    keys = [sorted(row, reverse=True) for row in bit_arrays]
    return sorted(range(n), key=lambda i: keys[i], reverse=True)

# ---- tests
import random
assert sort_binary_numbers([[0, 2], [2, 3], [2, 1]]) == [1, 2, 0]
assert sort_binary_numbers([[0, 1, 2], [3, 1, 0]]) == [1, 0]
for _ in range(300):
    m = random.randint(1, 4); n = random.randint(1, 6)
    rows = set()
    while len(rows) < n:
        rows.add(tuple(random.sample(range(0, 8), m)))
        if len(rows) < n and len(rows) >= 8 * 7: break
    rows = [list(r) for r in rows]
    val = lambda r: sum(1 << b for b in r)
    exp = sorted(range(len(rows)), key=lambda i: -val(rows[i]))
    assert sort_binary_numbers(rows) == exp
    # sets must be distinct as numbers
print('ok')

def spiral_order(matrix):
    if not matrix:
        return []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        out.extend(matrix[top][left:right + 1])
        for r in range(top + 1, bottom + 1):
            out.append(matrix[r][right])
        if top < bottom:
            out.extend(matrix[bottom][left:right][::-1])
        if left < right:
            for r in range(bottom - 1, top, -1):
                out.append(matrix[r][left])
        top += 1; bottom -= 1; left += 1; right -= 1
    return out

# ---- tests
import random
assert spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
assert spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
assert spiral_order([]) == []
def brute(m):
    m = [row[:] for row in m]
    out = []
    while m:
        out += m.pop(0)
        m = [list(r) for r in zip(*m)][::-1]      # rotate the remainder counter-clockwise
    return out
for _ in range(300):
    R, C = random.randint(1, 6), random.randint(1, 6)
    m = [[random.randint(0, 99) for _ in range(C)] for _ in range(R)]
    assert spiral_order(m) == brute(m)
print('ok')

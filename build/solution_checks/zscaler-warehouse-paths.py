MOD = 10**9 + 7


def num_paths(warehouse):
    rows, cols = len(warehouse), len(warehouse[0])
    paths = [[0] * cols for _ in range(rows)]
    if warehouse[0][0] == 1:
        paths[0][0] = 1
    for i in range(rows):
        for j in range(cols):
            if warehouse[i][j] == 1 and (i or j):
                from_up = paths[i - 1][j] if i else 0
                from_left = paths[i][j - 1] if j else 0
                paths[i][j] = (from_up + from_left) % MOD
    return paths[-1][-1] % MOD

# ---- tests
import random
assert num_paths([[1, 1], [1, 1]]) == 2
assert num_paths([[1, 0], [1, 1]]) == 1
assert num_paths([[0, 1], [1, 1]]) == 0
assert num_paths([[1]]) == 1
def brute(w):
    R, C = len(w), len(w[0])
    def go(i, j):
        if i >= R or j >= C or w[i][j] != 1: return 0
        if i == R - 1 and j == C - 1: return 1
        return go(i + 1, j) + go(i, j + 1)
    return go(0, 0)
for _ in range(300):
    R, C = random.randint(1, 6), random.randint(1, 6)
    w = [[1 if random.random() < .8 else 0 for _ in range(C)] for _ in range(R)]
    assert num_paths(w) == brute(w) % MOD
print('ok')

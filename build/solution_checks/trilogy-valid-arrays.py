MOD = 10**9 + 7


def count_valid(a, b, c):
    """Arrays of length a over [1, c] with no run of equal values longer than b."""
    first = []                                    # u[1..b] computed directly
    for n in range(1, min(a, b) + 1):
        total = c % MOD                           # one run covering everything
        total += (c - 1) * sum(first[n - j - 1] for j in range(1, n)) % MOD
        first.append(total % MOD)
    if a <= b:
        return first[a - 1]
    # u[n] = (c-1) * (u[n-1] + ... + u[n-b]) for n > b : linear recurrence of order b
    coef = (c - 1) % MOD
    # companion-matrix power on the state (u[n], u[n-1], ..., u[n-b+1])
    size = b
    mat = [[0] * size for _ in range(size)]
    for j in range(size):
        mat[0][j] = coef
    for i in range(1, size):
        mat[i][i - 1] = 1

    def mul(x, y):
        yt = list(zip(*y))
        return [[sum(p * q for p, q in zip(row, col)) % MOD for col in yt] for row in x]

    power = a - b
    result = [[int(i == j) for j in range(size)] for i in range(size)]
    while power:
        if power & 1:
            result = mul(result, mat)
        mat = mul(mat, mat)
        power >>= 1
    state = first[::-1]                            # (u[b], u[b-1], ..., u[1])
    return sum(result[0][j] * state[j] for j in range(size)) % MOD

# ---- tests
import random
from itertools import product
assert count_valid(3, 1, 3) == 12
assert count_valid(3, 3, 2) == 8
def brute(a, b, c):
    cnt = 0
    for arr in product(range(c), repeat=a):
        run = 1; ok = True
        for i in range(1, a):
            run = run + 1 if arr[i] == arr[i - 1] else 1
            if run > b: ok = False; break
        if ok: cnt += 1
    return cnt
for _ in range(200):
    a = random.randint(1, 8); b = random.randint(1, min(4, a)); c = random.randint(1, 4)
    assert count_valid(a, b, c) == brute(a, b, c) % MOD, (a, b, c)
count_valid(10**9, 50, 10**5)
print('ok')

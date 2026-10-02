def employee_year(n, m, a):
    basis = {}                                       # pivot bit -> vector; Gaussian elimination over GF(2)
    rank = 0
    for row in a:
        v = 0
        for j, x in enumerate(row):
            if x & 1:
                v |= 1 << j
        while v:
            p = v.bit_length() - 1
            if p in basis:
                v ^= basis[p]
            else:
                basis[p] = v
                rank += 1
                break
    return (1 << (n - rank)) - 1                      # subsets with XOR 0, minus the empty one

# ---- tests
import random
assert employee_year(2, 2, [[4, 4], [6, 6]]) == 3
def brute(n, m, a):
    cnt = 0
    for mask in range(1, 1 << n):
        if all(sum(a[i][j] for i in range(n) if mask >> i & 1) % 2 == 0 for j in range(m)): cnt += 1
    return cnt
for _ in range(300):
    n = random.randint(1, 7); m = random.randint(1, 4)
    a = [[random.randint(0, 9) for _ in range(m)] for _ in range(n)]
    assert employee_year(n, m, a) == brute(n, m, a)
print('ok')

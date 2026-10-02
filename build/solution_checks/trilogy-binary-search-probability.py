MOD = 10**9 + 7
MAXN = 10**6


def build_found_table(limit):
    """F[n] = how many of the n targets in a range of length n make the loop print Found."""
    F = [0] * (limit + 1)
    for n in range(2, limit + 1):
        left = (n - 1) // 2                  # elements strictly left of mid
        F[n] = 1 + F[left] + F[n - 1 - left]
    return F


F = build_found_table(MAXN)


def answer_queries(queries):
    out = []
    for l, r in queries:
        n = r - l + 1
        out.append((n - F[n]) * pow(n, MOD - 2, MOD) % MOD)   # P(fail) = (n - found) / n
    return out

# ---- tests
assert answer_queries([[2, 9]]) == [500000004]
assert answer_queries([[10, 10], [10, 12]]) == [1, 666666672]
def sim(l, r):
    found = 0
    for i in range(l, r + 1):
        a, b = l, r
        while a < b:
            mid = (a + b) // 2
            if i < mid: b = mid - 1
            elif i > mid: a = mid + 1
            else: found += 1; break
    return found
for l in range(1, 25):
    for r in range(l, 60):
        assert sim(l, r) == F[r - l + 1], (l, r)
print('ok')

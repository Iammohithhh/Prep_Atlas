def tech_club(n, k):
    count = 0
    cols = [False] * k
    d1 = [False] * (2 * k)
    d2 = [False] * (2 * k)

    def go(row, chosen):
        nonlocal count
        if chosen == n:
            count += 1
            return
        if k - row < n - chosen:                       # not enough rows left
            return
        for r in range(row, k):
            for c in range(k):
                if cols[c] or d1[r - c + k] or d2[r + c]:
                    continue
                cols[c] = d1[r - c + k] = d2[r + c] = True
                go(r + 1, chosen + 1)
                cols[c] = d1[r - c + k] = d2[r + c] = False
    go(0, 0)
    return count

# ---- tests
from itertools import combinations
assert tech_club(2, 3) == 8
assert tech_club(2, 2) == 0
def brute(n, k):
    cells = [(m, p) for m in range(k) for p in range(k)]
    cnt = 0
    for comb in combinations(cells, n):
        ok = True
        for (a, b), (c, d) in combinations(comb, 2):
            if a == c or b == d or abs(a - c) == abs(b - d): ok = False; break
        cnt += ok
    return cnt
for n in range(1, 4):
    for k in range(1, 6):
        assert tech_club(n, k) == brute(n, k), (n, k)
print('ok')

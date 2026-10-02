def first_occurrence(A, B):
    n, m = len(A), len(B)
    # nxt[p][c] = smallest index >= p holding letter c (n if none)
    nxt = [[n] * 26 for _ in range(n + 2)]
    for p in range(n - 1, -1, -1):
        nxt[p] = nxt[p + 1][:]
        nxt[p][ord(A[p]) - 97] = p
    # suf[j] = largest p such that B[j:] is a subsequence of A[p:] (-1 if impossible); suf[m] = n
    suf = [-1] * (m + 1)
    suf[m] = n
    p = n
    for j in range(m - 1, -1, -1):
        p -= 1
        while p >= 0 and A[p] != B[j]:
            p -= 1
        if p < 0:
            break
        suf[j] = p
    for i in range(n):
        if A[i] != B[0]:
            continue
        f = [i]                                       # earliest greedy match positions of B[0], B[1], ...
        while len(f) < m:
            pos = nxt[f[-1] + 1][ord(B[len(f)]) - 97]
            if pos >= n:
                break
            f.append(pos)
        if len(f) == m:                               # matches with no change
            return i + 1
        for j in range(1, len(f) + 1):                # use the single change on B[j] (j >= 1)
            q0 = f[j - 1] + 1                         # the changed letter takes the very next character
            if q0 >= n:
                continue
            if j == m - 1 or (suf[j + 1] != -1 and suf[j + 1] >= q0 + 1):
                return i + 1
    return -1

# ---- tests
import random
assert first_occurrence("daabe", "abe") == 2
assert first_occurrence("abcbc", "cba") == 3
assert first_occurrence("lhs", "rhs") == -1
def brute(A, B):
    n, m = len(A), len(B)
    for i in range(n):
        if A[i] != B[0]: continue
        # dp over (position in B, changes used) with greedy not possible; enumerate via DP on indices
        from functools import lru_cache
        @lru_cache(None)
        def go(pa, j, used):
            if j == m: return True
            for q in range(pa, n):
                if A[q] == B[j] and go(q + 1, j + 1, used): return True
                if A[q] != B[j] and not used and j >= 1 and go(q + 1, j + 1, True): return True
            return False
        if go(i + 1, 1, False): return i + 1
    return -1
for _ in range(1500):
    A = ''.join(random.choice('abc') for _ in range(random.randint(1, 9)))
    B = ''.join(random.choice('abc') for _ in range(random.randint(1, 5)))
    assert first_occurrence(A, B) == brute(A, B), (A, B)
print('ok')

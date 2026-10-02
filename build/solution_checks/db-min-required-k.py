import random
from itertools import combinations

def MinReq(N, A, B, M):
    sumA = sum(A)
    cnt = [sum(1 for a in A if a >> b & 1) for b in range(31)]
    val = []
    for b in B:
        and_sum = sum((1 << bit) * cnt[bit] for bit in range(31) if b >> bit & 1)
        val.append(sumA + N * b - and_sum)       # sum of (a | b) over all a
    if M == 0:
        return 0
    NEG = float('-inf')
    maxK = (N + 1) // 2
    # best[i][k] = max sum choosing k non-adjacent among first i, i.e. dp with take/skip
    prev2 = [0] + [NEG] * maxK                    # dp[i-2]
    prev1 = [0] + [NEG] * maxK                    # dp[i-1] (i = 0 -> empty prefix)
    # dp[i][k] = max(dp[i-1][k], dp[i-2][k-1] + val[i-1])
    dp_prev2 = [0] + [NEG] * maxK
    dp_prev1 = [0] + [NEG] * maxK
    for i in range(1, N + 1):
        cur = dp_prev1[:]
        for k in range(1, maxK + 1):
            if dp_prev2[k - 1] > NEG:
                cur[k] = max(cur[k], dp_prev2[k - 1] + val[i - 1])
        dp_prev2, dp_prev1 = dp_prev1, cur
    for k in range(maxK + 1):
        if dp_prev1[k] >= M:
            return k
    return -1

def brute(N, A, B, M):
    val = [sum(a | b for a in A) for b in B]
    for k in range(0, N + 1):
        for idx in combinations(range(N), k):
            if all(idx[i + 1] - idx[i] > 1 for i in range(len(idx) - 1)):
                if sum(val[i] for i in idx) >= M:
                    return k
    return -1

assert MinReq(5, [1, 2, 3, 4, 5], [2, 2, 2, 2, 2], 40) == 2
for _ in range(300):
    n = random.randint(1, 7)
    A = [random.randint(0, 15) for _ in range(n)]
    B = [random.randint(0, 15) for _ in range(n)]
    M = random.randint(0, 150)
    assert MinReq(n, A, B, M) == brute(n, A, B, M), (A, B, M)
print('ok')

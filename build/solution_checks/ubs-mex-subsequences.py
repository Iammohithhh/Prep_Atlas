MOD = 10**9 + 7


def count_subsequences(arr, l, r):
    n = len(arr)
    cnt = {}
    for v in arr:
        cnt[v] = cnt.get(v, 0) + 1
    pw = [1] * (n + 1)
    for i in range(1, n + 1):
        pw[i] = pw[i - 1] * 2 % MOD
    total = 0
    prod = 1                                        # prod over v < m of (2^cnt[v] - 1)
    prefix = 0                                      # number of elements with value < m
    for m in range(0, min(r, n) + 1):
        # subsequences with MEX exactly m: take >=1 of each 0..m-1, none of value m, anything of value > m
        if m >= l:
            free = n - prefix - cnt.get(m, 0)
            total = (total + prod * pw[free]) % MOD
        c = cnt.get(m, 0)
        if c == 0:
            break                                   # larger MEX values are impossible
        prod = prod * (pw[c] - 1) % MOD
        prefix += c
    return total

# ---- tests
import random
assert count_subsequences([0, 1, 2], 1, 2) == 3
assert count_subsequences([0, 2, 4, 1, 0], 2, 3) == 12
def mex(s):
    m = 0
    S = set(s)
    while m in S: m += 1
    return m
def brute(arr, l, r):
    n = len(arr); t = 0
    for mask in range(1 << n):
        sub = [arr[i] for i in range(n) if mask >> i & 1]
        if l <= mex(sub) <= r: t += 1
    return t % MOD
for _ in range(500):
    arr = [random.randint(0, 4) for _ in range(random.randint(1, 10))]
    l = random.randint(0, 4); r = random.randint(l, 5)
    assert count_subsequences(arr, l, r) == brute(arr, l, r), (arr, l, r)
print('ok')

MOD = 10**9 + 7


def count_permutations(n, a):
    """a[i] = number of visible notifications after i+1 arrivals."""
    if a[0] != 1:
        return 0
    last = {0: 0}                      # last[level] = 1-based index of the latest element at that stack size
    pg = [0] * (n + 2)                 # previous-greater index (0 = none)
    for i in range(1, n + 1):
        h = a[i - 1]
        if h < 1 or h - 1 not in last:
            return 0
        pg[i] = last[h - 1]
        last[h] = i
        for key in [k for k in last if k > h]:     # deeper levels are closed
            del last[key]
    # end[i] = last position of i's subtree = (next index with level <= level_i) - 1
    end = [n] * (n + 2)
    stack = []
    for i in range(1, n + 1):
        while stack and a[stack[-1] - 1] >= a[i - 1]:
            end[stack.pop()] = i - 1
        stack.append(i)
    fact = 1
    for v in range(2, n + 1):
        fact = fact * v % MOD
    denom = 1
    for i in range(1, n + 1):
        denom = denom * (end[i] - pg[i]) % MOD
    return fact * pow(denom, MOD - 2, MOD) % MOD

# ---- tests
from itertools import permutations
from collections import Counter
assert count_permutations(5, [1, 2, 3, 1, 2]) == 4
def logs(p):
    st = []; res = []
    for v in p:
        while st and st[-1] < v: st.pop()
        st.append(v); res.append(len(st))
    return tuple(res)
for n in range(1, 8):
    cnt = Counter(logs(p) for p in permutations(range(n)))
    for log, c in cnt.items():
        assert count_permutations(n, list(log)) == c, (n, log)
    assert count_permutations(n, [2] + [1] * (n - 1)) == 0
    if n > 2:
        assert count_permutations(n, [1, 3] + [1] * (n - 2)) == 0
print('ok')

import random
from collections import Counter

def findLongestSubsequence(arr):
    cnt = Counter(arr)
    vals = sorted(cnt)
    pre = {}
    s = 0
    for v in vals:
        s += cnt[v]
        pre[v] = s
    last = {}                                   # farthest value of each parity
    for v in vals:
        last[v % 2] = v
    best = 1
    for lo in vals:
        hi = last[lo % 2]                       # farthest same-parity maximum
        best = max(best, pre[hi] - (pre[lo] - cnt[lo]))
    return best

def brute(arr):
    n = len(arr)
    best = 0
    for mask in range(1, 1 << n):
        sub = sorted(arr[i] for i in range(n) if mask >> i & 1)
        if (sub[-1] - sub[0]) % 2 == 0:
            best = max(best, len(sub))
    return best

assert findLongestSubsequence([7, 5, 6, 2, 3, 2, 4]) == 6
assert findLongestSubsequence([1, 3, 5, 7]) == 4
assert findLongestSubsequence([2, 4, 1, 7]) == 4
for _ in range(300):
    a = [random.randint(0, 9) for _ in range(random.randint(1, 10))]
    assert findLongestSubsequence(a) == brute(a), a
print('ok')

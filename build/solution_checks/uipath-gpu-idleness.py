import random

def findMinimumIdleness(shader, switchCount):
    n = len(shader)
    def cost(L):
        if L == 1:
            a = sum(1 for i, c in enumerate(shader) if c != 'ab'[i % 2])
            return min(a, n - a)
        total, i = 0, 0
        while i < n:
            j = i
            while j < n and shader[j] == shader[i]:
                j += 1
            total += (j - i) // (L + 1)
            i = j
        return total
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if cost(mid) <= switchCount:
            hi = mid
        else:
            lo = mid + 1
    return lo

def brute(s, k):
    n = len(s)
    best = n
    for mask in range(1 << n):
        if bin(mask).count('1') > k:
            continue
        t = [('b' if c == 'a' else 'a') if mask >> i & 1 else c for i, c in enumerate(s)]
        run = mx = 1
        for i in range(1, n):
            run = run + 1 if t[i] == t[i - 1] else 1
            mx = max(mx, run)
        best = min(best, mx)
    return best

assert findMinimumIdleness('aaaaa', 1) == 2
assert findMinimumIdleness('aabbbaaaa', 2) == 2
for _ in range(500):
    n = random.randint(1, 10)
    s = ''.join(random.choice('ab') for _ in range(n))
    k = random.randint(1, n)
    assert findMinimumIdleness(s, k) == brute(s, k), (s, k)
print('ok')

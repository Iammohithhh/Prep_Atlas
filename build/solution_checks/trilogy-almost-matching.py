def count_pairs(s, k):
    n = len(s)
    # lcp[i][j] = length of the longest common prefix of s[i:] and s[j:]
    lcp = [[0] * (n + 2) for _ in range(n + 2)]
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if s[i] == s[j]:
                lcp[i][j] = 1 + lcp[i + 1][j + 1]
    total = 0
    for i in range(n):
        for l in range(n):
            if i == l or i + k >= n or l + k >= n:
                continue
            if lcp[i][l] < k:                      # the first k characters must agree
                continue
            if s[i + k] == s[l + k]:               # they must differ at position k
                continue
            # lengths k+1 .. k+1+lcp(after the differing position); each is one pair
            total += 1 + lcp[i + k + 1][l + k + 1]
    return total

# ---- tests
import random
assert count_pairs("abacaba", 1) == 8
def brute(s, k):
    n = len(s); cnt = 0
    subs = [(i, j) for i in range(n) for j in range(i, n)]
    for (i, j) in subs:
        for (l, m) in subs:
            if j - i != m - l or j - i < k: continue
            a, b = s[i:j + 1], s[l:m + 1]
            diff = [t for t in range(len(a)) if a[t] != b[t]]
            if diff == [k]: cnt += 1
    return cnt
for _ in range(200):
    s = ''.join(random.choice('abc') for _ in range(random.randint(1, 9)))
    k = random.randint(0, len(s) - 1)
    assert count_pairs(s, k) == brute(s, k), (s, k)
print('ok')

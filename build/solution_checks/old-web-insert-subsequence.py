def max_occurrences_after_insert(s, t):
    n, m = len(t), len(s)
    # f[i][j]: ways to form s[:j] as a subsequence of t[:i];  g[i][j]: ways to form s[j:] from t[i:]
    f = [[0] * (m + 1) for _ in range(n + 1)]
    g = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        f[i][0] = 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            f[i][j] = f[i - 1][j] + (f[i - 1][j - 1] if t[i - 1] == s[j - 1] else 0)
    for i in range(n + 1):
        g[i][m] = 1
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            g[i][j] = g[i + 1][j] + (g[i + 1][j + 1] if t[i] == s[j] else 0)
    base = f[n][m]
    best_gain = 0
    for i in range(n + 1):                   # insert between t[:i] and t[i:]
        gain = {}
        for j in range(m):
            gain[s[j]] = gain.get(s[j], 0) + f[i][j] * g[i][j + 1]
        if gain:
            best_gain = max(best_gain, max(gain.values()))
    return base + best_gain

# ---- tests
import random
def count(s, t):
    dp = [1] + [0] * len(s)
    for ch in t:
        for j in range(len(s), 0, -1):
            if s[j - 1] == ch:
                dp[j] += dp[j - 1]
    return dp[len(s)]
def brute(s, t):
    best = 0
    for i in range(len(t) + 1):
        for ch in set(s) | {'z'}:
            best = max(best, count(s, t[:i] + ch + t[i:]))
    return best
assert max_occurrences_after_insert("ab", "ab") == 2
for _ in range(500):
    s = ''.join(random.choice('ab') for _ in range(random.randint(1, 3)))
    t = ''.join(random.choice('ab') for _ in range(random.randint(0, 7)))
    assert max_occurrences_after_insert(s, t) == brute(s, t), (s, t)
print('ok')

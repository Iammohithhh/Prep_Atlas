def count_move_subsequences(moves, n, x, y):
    dp = [0] * (n + 1)
    dp[x] = 1                                        # the empty string ends at x
    last = {'l': [0] * (n + 1), 'r': [0] * (n + 1)}  # extensions created by the previous occurrence of each letter
    for c in moves:
        ext = [0] * (n + 1)
        step = -1 if c == 'l' else 1
        for p in range(n + 1):
            if dp[p]:
                q = p + step
                if 0 <= q <= n:
                    ext[q] += dp[p]
        for p in range(n + 1):
            dp[p] += ext[p] - last[c][p]             # only strings not already produced by an earlier occurrence
        last[c] = ext
    return dp[y]

# ---- tests
import random
from itertools import combinations
assert count_move_subsequences("rrlrlr", 6, 1, 4) == 3
def brute(moves, n, x, y):
    seen = set()
    L = len(moves)
    for mask in range(1 << L):
        s = ''.join(moves[i] for i in range(L) if mask >> i & 1)
        pos = x; ok = True
        for ch in s:
            pos += 1 if ch == 'r' else -1
            if not 0 <= pos <= n: ok = False; break
        if ok and pos == y: seen.add(s)
    return len(seen)
for _ in range(400):
    L = random.randint(1, 10); mv = ''.join(random.choice('lr') for _ in range(L)); n = random.randint(1, 6)
    x, y = random.randint(0, n), random.randint(0, n)
    assert count_move_subsequences(mv, n, x, y) == brute(mv, n, x, y), (mv, n, x, y)
print('ok')

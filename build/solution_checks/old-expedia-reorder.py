def get_min_steps(current, desired):
    n = len(current)
    k = 0                                     # length of the longest prefix of current that is a subsequence of desired
    for x in desired:
        if k < n and x == current[k]:
            k += 1
    return n - k

# ---- tests
import random
from collections import deque
assert get_min_steps([2, 1, 3, 5, 4], [2, 4, 1, 5, 3]) == 2
def brute(cur, des):
    cur, des = tuple(cur), tuple(des)
    dist = {cur: 0}
    q = deque([cur])
    while q:
        s = q.popleft()
        if s == des:
            return dist[s]
        last, rest = s[-1], s[:-1]
        for pos in range(len(s)):
            t = rest[:pos] + (last,) + rest[pos:]
            if t not in dist:
                dist[t] = dist[s] + 1
                q.append(t)
for _ in range(300):
    n = random.randint(1, 6)
    cur = list(range(1, n + 1)); des = cur[:]
    random.shuffle(cur); random.shuffle(des)
    assert get_min_steps(cur, des) == brute(cur, des), (cur, des)
print('ok')

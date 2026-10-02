def tower_days(n, arr):
    arrived = [False] * (n + 2)
    need = n                        # the largest brick not yet placed
    out = []
    for size in arr:
        arrived[size] = True
        today = []
        while need >= 1 and arrived[need]:
            today.append(need)
            need -= 1
        out.append(today)
    return out

# ---- tests
import random
assert tower_days(5, [4, 5, 1, 2, 3]) == [[], [5, 4], [], [], [3, 2, 1]]
assert tower_days(1, [1]) == [[1]]
for _ in range(200):
    n = random.randint(1, 8); p = list(range(1, n + 1)); random.shuffle(p)
    res = tower_days(n, p)
    flat = [x for r in res for x in r]
    assert flat == list(range(n, 0, -1))           # every brick placed exactly once, largest first
print('ok')

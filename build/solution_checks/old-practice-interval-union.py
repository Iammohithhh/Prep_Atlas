def covered_length(intervals):
    total = 0
    cur_s = cur_e = None
    for s, e in sorted(intervals):
        if cur_e is None or s > cur_e:
            if cur_e is not None:
                total += cur_e - cur_s
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
    if cur_e is not None:
        total += cur_e - cur_s
    return total

# ---- tests
import random
assert covered_length([]) == 0
assert covered_length([[1, 3], [2, 6], [8, 10]]) == 7
assert covered_length([[1, 1], [2, 2]]) == 0
assert covered_length([[1, 5], [2, 3]]) == 4
def brute(iv):
    cells = set()
    for s, e in iv:
        for x in range(s, e):                 # unit segment [x, x+1]
            cells.add(x)
    return len(cells)
for _ in range(400):
    iv = []
    for _ in range(random.randint(0, 7)):
        a = random.randint(-5, 10); iv.append([a, a + random.randint(0, 6)])
    assert covered_length(iv) == brute(iv)
print('ok')

def merge_intervals(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)       # overlapping or touching
        else:
            out.append([s, e])
    return out

# ---- tests
import random
assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
assert merge_intervals([]) == []
def brute(iv):
    pts = set()
    for s, e in iv:
        pts.update(range(2 * s, 2 * e + 1))       # doubled coordinates: closed interval as a point set
    res = []
    for p in sorted(pts):
        if res and p == res[-1][1] + 1:
            res[-1][1] = p
        else:
            res.append([p, p])
    return [[a // 2, b // 2] for a, b in res]
for _ in range(400):
    iv = []
    for _ in range(random.randint(0, 7)):
        a = random.randint(-5, 10); iv.append([a, a + random.randint(0, 5)])
    assert merge_intervals([x[:] for x in iv]) == brute(iv), iv
print('ok')

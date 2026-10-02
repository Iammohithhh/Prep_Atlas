from bisect import bisect_left


def choose_flask(requirements, flask_types, markings):
    req = sorted(requirements)
    n = len(req)
    prefix = [0]
    for r in req:
        prefix.append(prefix[-1] + r)
    marks = [[] for _ in range(flask_types)]
    for f, m in markings:
        marks[f].append(m)
    best_waste, best_idx = None, -1
    for f in range(flask_types):
        ms = sorted(set(marks[f]))
        if not ms or ms[-1] < req[-1]:
            continue                                   # cannot satisfy the largest order
        waste = 0
        lo = 0                                         # first requirement not yet assigned to a marking
        for m in ms:
            hi = bisect_left(req, m + 1)               # requirements <= m
            if hi > lo:
                waste += m * (hi - lo) - (prefix[hi] - prefix[lo])
                lo = hi
            if lo == n:
                break
        if best_waste is None or waste < best_waste:
            best_waste, best_idx = waste, f
    return best_idx

# ---- tests
import random
assert choose_flask([4, 6], 2, [[0, 5], [0, 7], [0, 10], [1, 4], [1, 10]]) == 0
assert choose_flask([10, 15], 3, [[0, 11], [0, 20], [1, 11], [1, 17], [2, 12], [2, 16]]) == 1
assert choose_flask([4, 6, 6, 7], 3, [[0, 3], [0, 5], [0, 7], [1, 6], [1, 8], [1, 9], [2, 3], [2, 5], [2, 6]]) == 0
def brute(req, ft, mk):
    best = None; bi = -1
    for f in range(ft):
        ms = [m for ff, m in mk if ff == f]; w = 0; ok = True
        for r in req:
            c = [m for m in ms if m >= r]
            if not c: ok = False; break
            w += min(c) - r
        if ok and (best is None or w < best): best, bi = w, f
    return bi
for _ in range(300):
    n = random.randint(1, 6); ft = random.randint(1, 4)
    req = [random.randint(1, 15) for _ in range(n)]
    mk = [[random.randrange(ft), random.randint(0, 20)] for _ in range(random.randint(1, 10))]
    assert choose_flask(req, ft, mk) == brute(req, ft, mk), (req, ft, mk)
print('ok')

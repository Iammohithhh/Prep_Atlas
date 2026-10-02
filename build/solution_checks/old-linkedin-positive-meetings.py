def max_meetings(effectiveness):
    total = 0
    count = 0
    for v in sorted(effectiveness, reverse=True):
        total += v
        if total <= 0:
            break
        count += 1
    return count

# ---- tests
import random
from itertools import permutations
assert max_meetings([1, -20, 3, -2]) == 3
assert max_meetings([-3, 0, 2, 1]) == 3
def brute(e):
    best = 0
    for perm in permutations(e):
        s = 0; c = 0
        for v in perm:
            s += v
            if s <= 0:
                break
            c += 1
        best = max(best, c)
    return best
for _ in range(300):
    e = [random.randint(-5, 5) for _ in range(random.randint(1, 6))]
    assert max_meetings(e) == brute(e), e
print('ok')

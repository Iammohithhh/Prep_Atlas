def min_speed(ev_batteries, total_hours):
    lo, hi = 1, max(ev_batteries)

    def hours(speed):
        return sum((b + speed - 1) // speed for b in ev_batteries)

    while lo < hi:
        mid = (lo + hi) // 2
        if hours(mid) <= total_hours:
            hi = mid
        else:
            lo = mid + 1
    return lo

# ---- tests
import random
assert min_speed([120, 180, 240, 60], 6) == 120
def brute(b, h):
    for s in range(1, max(b) + 1):
        if sum(-(-x // s) for x in b) <= h: return s
for _ in range(300):
    b = [random.randint(1, 50) for _ in range(random.randint(1, 6))]
    h = random.randint(len(b), len(b) + 20)
    assert min_speed(b, h) == brute(b, h)
print('ok')

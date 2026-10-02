def get_min_max_parcels(parcels, extra_parcels):
    n = len(parcels)
    total = sum(parcels) + extra_parcels
    return max(max(parcels), (total + n - 1) // n)

# ---- tests
import random
from itertools import product
assert get_min_max_parcels([7, 5, 1, 9, 1], 25) == 10
assert get_min_max_parcels([1, 2, 3], 3) == 3
def brute(p, e):
    best = 10**9
    for add in product(range(e + 1), repeat=len(p)):
        if sum(add) == e: best = min(best, max(x + y for x, y in zip(p, add)))
    return best
for _ in range(300):
    p = [random.randint(0, 6) for _ in range(random.randint(1, 4))]; e = random.randint(0, 6)
    assert get_min_max_parcels(p, e) == brute(p, e)
print('ok')

def max_requests_handled(server_capacity, incoming, k):
    base = sum(min(c, r) for c, r in zip(server_capacity, incoming))
    gains = sorted((min(2 * c, r) - min(c, r) for c, r in zip(server_capacity, incoming)), reverse=True)
    return base + sum(gains[:k])

# ---- tests
import random
from itertools import combinations
assert max_requests_handled([10, 4, 3, 7], [3, 10, 4, 5], 2) == 20
for _ in range(300):
    n = random.randint(1, 7); cap = [random.randint(1, 10) for _ in range(n)]; req = [random.randint(1, 20) for _ in range(n)]
    k = random.randint(0, n)
    best = max(sum(min(c * (2 if i in S else 1), r) for i, (c, r) in enumerate(zip(cap, req))) for S in combinations(range(n), k))
    assert max_requests_handled(cap, req, k) == best
print('ok')

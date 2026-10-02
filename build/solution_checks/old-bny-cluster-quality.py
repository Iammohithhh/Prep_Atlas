import heapq


def max_cluster_quality(speed, reliability, max_machines):
    machines = sorted(zip(reliability, speed), reverse=True)
    heap, total, best = [], 0, 0
    for rel, sp in machines:
        heapq.heappush(heap, sp)
        total += sp
        if len(heap) > max_machines:
            total -= heapq.heappop(heap)
        best = max(best, total * rel)
    return best

# ---- tests
import random
from itertools import combinations
assert max_cluster_quality([4, 3, 15, 5, 6], [7, 6, 1, 2, 8], 3) == 78
assert max_cluster_quality([12, 112, 100, 13, 55], [31, 4, 100, 55, 50], 3) == 10000
def brute(sp, rel, k):
    best = 0
    n = len(sp)
    for r in range(1, k + 1):
        for c in combinations(range(n), r):
            best = max(best, sum(sp[i] for i in c) * min(rel[i] for i in c))
    return best
for _ in range(300):
    n = random.randint(1, 7)
    sp = [random.randint(1, 9) for _ in range(n)]
    rel = [random.randint(1, 9) for _ in range(n)]
    k = random.randint(1, n)
    assert max_cluster_quality(sp, rel, k) == brute(sp, rel, k)
print('ok')

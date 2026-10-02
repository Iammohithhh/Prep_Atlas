import heapq


def min_total_fare(n, x, cost):
    heap = [-c for c in cost]          # max-heap via negation
    heapq.heapify(heap)
    for _ in range(x):
        top = -heap[0]
        if top == 0:                    # nothing left to reduce
            break
        heapq.heapreplace(heap, -(top // 2))
    return -sum(heap)

# ---- tests
import random
assert min_total_fare(4, 2, [1, 2, 4, 128]) == 39
def brute(n, x, cost):
    best = [10**18]
    def go(i, left, tot):
        if i == n:
            best[0] = min(best[0], tot); return
        c = cost[i]
        for k in range(left + 1):
            go(i + 1, left - k, tot + (c >> k))
    go(0, x, 0)
    return best[0]
for _ in range(300):
    n = random.randint(1, 5); x = random.randint(0, 6)
    c = [random.randint(1, 60) for _ in range(n)]
    assert min_total_fare(n, x, c) == brute(n, x, c), (n, x, c)
print('ok')

import random, heapq
from bisect import bisect_right

def served(events, lawyers, c, t):
    heap = []; li = 0
    L = sorted(lawyers) + [t]
    L.sort(key=lambda x: (x, 1 if x == t else 0))
    # Mike is represented by value t; ties cannot occur for valid t
    L = sorted(lawyers + [t])
    for e in sorted(events):
        while li < len(L) and L[li] <= e:
            heapq.heappush(heap, L[li]); li += 1
        for _ in range(c):
            if not heap: break
            if heapq.heappop(heap) == t: return True
    return False

def latestArrival(events, lawyers, c):
    taken = set(lawyers)

    def free(x):                            # largest unused time <= x, or -1
        while x >= 0 and x in taken:
            x -= 1
        return x

    def bad(x):                             # monotone: once True it stays True
        f = free(x)
        return f >= 0 and not served(events, lawyers, c, f)

    lo, hi, best = 0, max(events), -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if not bad(mid):
            best = mid; lo = mid + 1
        else:
            hi = mid - 1
    return free(best) if best >= 0 else -1

def brute(events, lawyers, c):
    taken = set(lawyers)
    best = -1
    for t in range(0, max(events) + 2):
        if t in taken: continue
        if served(events, lawyers, c, t): best = t
    return best

assert latestArrival([20, 30, 10], [19, 13, 26, 4, 25, 11, 21], 2) == 20
assert latestArrival([10, 20], [2, 17, 18, 19], 2) == 16
for _ in range(500):
    n = random.randint(1, 4); m = random.randint(1, 6)
    ev = random.sample(range(1, 25), n)
    lw = random.sample(range(0, 25), m)
    c = random.randint(1, 3)
    assert latestArrival(ev, lw, c) == brute(ev, lw, c), (ev, lw, c)
print('ok')

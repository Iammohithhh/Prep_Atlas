import random

def minPrice(N, x, a):
    best = None
    cur = a[:]                                    # cur[t] = cheapest price seen so far for type t
    for k in range(N):
        if k > 0:
            for t in range(N):
                cand = a[(t - k) % N]
                if cand < cur[t]:
                    cur[t] = cand
        total = k * x + sum(cur)
        best = total if best is None else min(best, total)
    return best

def brute(N, x, a):
    best = None
    for k in range(N):
        total = k * x
        for t in range(N):
            total += min(a[(t - j) % N] for j in range(k + 1))
        best = total if best is None else min(best, total)
    return best

assert minPrice(3, 5, [50, 1, 50]) == 13
for _ in range(300):
    n = random.randint(1, 8)
    x = random.randint(0, 20)
    a = [random.randint(1, 30) for _ in range(n)]
    assert minPrice(n, x, a) == brute(n, x, a)
print('ok')

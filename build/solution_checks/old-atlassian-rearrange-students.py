from collections import Counter


def rearrange_students(arr_a, arr_b):
    ca, cb = Counter(arr_a), Counter(arr_b)
    ex_a, ex_b = [], []
    for h in set(ca) | set(cb):
        if (ca[h] + cb[h]) % 2:
            return -1
        d = ca[h] - cb[h]
        if d > 0:
            ex_a += [h] * (d // 2)
        elif d < 0:
            ex_b += [h] * (-d // 2)
    g = min(min(arr_a), min(arr_b))
    ex_a.sort()
    ex_b.sort(reverse=True)
    return sum(min(a, b, 2 * g) for a, b in zip(ex_a, ex_b))

# ---- tests
import heapq, random
assert rearrange_students([4, 2, 2, 2], [1, 4, 1, 2]) == 1
assert rearrange_students([1, 2], [1, 3]) == -1
def brute(A, B):
    start = (tuple(sorted(A)), tuple(sorted(B)))
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, (a, b) = heapq.heappop(pq)
        if dist[(a, b)] < d:
            continue
        if a == b:
            return d
        for i in range(len(a)):
            for j in range(len(b)):
                na = list(a); nb = list(b)
                na[i], nb[j] = b[j], a[i]
                st = (tuple(sorted(na)), tuple(sorted(nb)))
                nd = d + min(a[i], b[j])
                if nd < dist.get(st, 1 << 60):
                    dist[st] = nd
                    heapq.heappush(pq, (nd, st))
    return -1
for _ in range(400):
    n = random.randint(1, 4)
    A = [random.randint(1, 5) for _ in range(n)]
    B = [random.randint(1, 5) for _ in range(n)]
    assert rearrange_students(A, B) == brute(A, B), (A, B)
print('ok')

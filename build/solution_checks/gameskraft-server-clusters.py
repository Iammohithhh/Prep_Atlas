def get_cluster_sizes(server_prop):
    n = len(server_prop)
    limit = max(server_prop) + 1
    parent = list(range(limit))
    size = [1] * limit

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    # smallest prime factor sieve
    spf = list(range(limit))
    for i in range(2, int(limit ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, limit, i):
                if spf[j] == j:
                    spf[j] = i
    # union every server value with each of its prime factors (nodes 0..limit are values / primes)
    for v in server_prop:
        x = v
        while x > 1:
            p = spf[x]
            union(v, p)
            while x % p == 0:
                x //= p
    count = {}
    for v in server_prop:
        if v > 1:
            r = find(v)
            count[r] = count.get(r, 0) + 1
    return [count[find(v)] if v > 1 else 1 for v in server_prop]

# ---- tests
import random
from math import gcd
assert get_cluster_sizes([1, 2, 4]) == [1, 2, 2]
assert get_cluster_sizes([3, 3, 3]) == [3, 3, 3]
def brute(p):
    n = len(p); par = list(range(n))
    def f(x):
        while par[x] != x: x = par[x]
        return x
    for i in range(n):
        for j in range(i + 1, n):
            if gcd(p[i], p[j]) > 1: par[f(i)] = f(j)
    cnt = {}
    for i in range(n): cnt[f(i)] = cnt.get(f(i), 0) + 1
    return [cnt[f(i)] for i in range(n)]
for _ in range(500):
    p = [random.randint(1, 60) for _ in range(random.randint(1, 12))]
    assert get_cluster_sizes(p) == brute(p), p
print('ok')

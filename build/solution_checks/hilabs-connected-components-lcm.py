import random
from math import gcd

def solve(N, arr, L=10**6):
    present = set(a for a in arr if a <= L)
    big = sum(1 for a in arr if a > L)          # a > L has lcm > L with everything
    parent = {a: a for a in present}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    firstdiv = [0] * (L + 1)
    for x in sorted(present):
        for m in range(x, L + 1, x):
            if firstdiv[m] == 0:
                firstdiv[m] = x
            else:
                parent[find(x)] = find(firstdiv[m])
    return big + len({find(a) for a in present})

def brute(arr, L):
    n = len(arr)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] * arr[j] // gcd(arr[i], arr[j]) <= L:
                parent[find(i)] = find(j)
    return len({find(i) for i in range(n)})

assert solve(3, [2, 1000000, 999999]) == 2
for _ in range(200):
    L = random.randint(5, 60)
    arr = random.sample(range(1, 80), random.randint(1, 10))
    assert solve(len(arr), arr, L) == brute(arr, L), (arr, L)
print('ok')

import random
def z_function(s):
    n = len(s); z = [0]*n; l = r = 0
    for i in range(1, n):
        if i < r: z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]: z[i] += 1
        if i + z[i] > r: l, r = i, i + z[i]
    return z

def minRotations(first, second):
    n = len(first)
    t = first + '\x00' + second + second
    z = z_function(t)
    best, bestcost = 0, 0
    for k in range(n):                       # k left rotations
        lcp = min(z[n + 1 + k], n)
        cost = min(k, n - k)                 # or n-k right rotations
        if lcp > best or (lcp == best and lcp > 0 and cost < bestcost):
            best, bestcost = lcp, cost
    return bestcost if best > 0 else -1

def brute(first, second):
    n = len(first); best = 0; bc = None
    for k in range(n):
        r = second[k:] + second[:k]
        l = 0
        while l < n and r[l] == first[l]: l += 1
        cost = min(k, n - k)
        if l > best or (l == best and l > 0 and cost < bc):
            best, bc = l, cost
    return bc if best > 0 else -1

assert minRotations('a2abccc', 'bddda2a') == 3
for _ in range(500):
    n = random.randint(1, 8)
    f = ''.join(random.choice('ab2') for _ in range(n))
    s = ''.join(random.choice('ab2') for _ in range(n))
    assert minRotations(f, s) == brute(f, s), (f, s)
print('ok')

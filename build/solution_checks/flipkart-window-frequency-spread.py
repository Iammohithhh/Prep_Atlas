def sum_of_spreads(n, k, a):
    freq = {}
    cc = {}                                          # frequency -> number of distinct values having it
    state = {'max': 0, 'min': 0}

    def bump(v, d):
        f = freq.get(v, 0)
        if f:
            cc[f] -= 1
            if cc[f] == 0:
                del cc[f]
        f += d
        if f:
            freq[v] = f
            cc[f] = cc.get(f, 0) + 1
        else:
            freq.pop(v, None)
        if cc:
            state['max'] = max(cc)
            state['min'] = min(cc)
        else:
            state['max'] = state['min'] = 0

    total = 0
    for i in range(n):
        bump(a[i], 1)
        if i >= k:
            bump(a[i - k], -1)
        if i >= k - 1:
            total += state['max'] - state['min']
    return total

# ---- tests
import random
assert sum_of_spreads(6, 3, [5, 5, 4, 4, 4, 4]) == 2
def brute(n, k, a):
    t = 0
    for i in range(n - k + 1):
        w = a[i:i + k]
        fs = [w.count(v) for v in set(w)]
        t += max(fs) - min(fs)
    return t
for _ in range(500):
    n = random.randint(1, 14); k = random.randint(1, n); a = [random.randint(1, 4) for _ in range(n)]
    assert sum_of_spreads(n, k, a) == brute(n, k, a)
print('ok')

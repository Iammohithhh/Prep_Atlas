MOD = 10**9 + 7


def count_strings(n, pairs):
    parent = list(range(26))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for a, b in pairs:                       # transitive closure = connected components
        parent[find(ord(a) - 97)] = find(ord(b) - 97)
    comp = [find(i) for i in range(26)]
    f = [1] * 26                             # strings of length 1 ending in each letter
    for _ in range(n - 1):
        total = sum(f) % MOD
        comp_sum = {}
        for ch in range(26):
            comp_sum[comp[ch]] = (comp_sum.get(comp[ch], 0) + f[ch]) % MOD
        # next letter ch may follow any letter outside its component, or ch itself
        f = [(total - comp_sum[comp[ch]] + f[ch]) % MOD for ch in range(26)]
    return sum(f) % MOD

# ---- tests
import random
from itertools import product
assert count_strings(2, [('a', 'b'), ('b', 'c'), ('c', 'd')]) == 26 * 26 - 12
assert count_strings(1, []) == 26
def brute(n, pairs):
    par = {chr(97 + i): chr(97 + i) for i in range(26)}
    def f(x):
        while par[x] != x: x = par[x]
        return x
    for a, b in pairs: par[f(a)] = f(b)
    letters = 'abcd'     # restrict alphabet to keep brute small; others behave as singletons
    cnt = 0
    for s in product(letters, repeat=n):
        if all(s[i] == s[i + 1] or f(s[i]) != f(s[i + 1]) for i in range(n - 1)): cnt += 1
    return cnt
for _ in range(100):
    n = random.randint(1, 4)
    pairs = [tuple(random.sample('abcd', 2)) for _ in range(random.randint(0, 3))]
    # compare on 4-letter alphabet by making the other 22 letters unusable is awkward; so recompute DP restricted
    got = count_strings(n, pairs)
    # full-alphabet brute for n <= 3 via product over 26 letters would be 17576 strings: fine
    if n <= 3:
        par = list(range(26))
        def ff(x):
            while par[x] != x: x = par[x]
            return x
        for a, b in pairs: par[ff(ord(a) - 97)] = ff(ord(b) - 97)
        cnt = 0
        for s in product(range(26), repeat=n):
            if all(s[i] == s[i + 1] or ff(s[i]) != ff(s[i + 1]) for i in range(n - 1)): cnt += 1
        assert got == cnt % MOD, (n, pairs)
print('ok')

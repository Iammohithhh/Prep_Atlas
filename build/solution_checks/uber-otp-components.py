def min_otps(n, otps):
    parent = list(range(26))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for s in otps:
        first = ord(s[0]) - 97
        for ch in s:
            ra, rb = find(first), find(ord(ch) - 97)
            if ra != rb:
                parent[ra] = rb
    # number of distinct letter-components that appear in some OTP
    return len({find(ord(s[0]) - 97) for s in otps})

# ---- tests
import random
assert min_otps(4, ["a", "b", "ab", "d"]) == 2
assert min_otps(1, ["uber"]) == 1
def brute(otps):
    n = len(otps); seen = [False] * n; comps = 0
    for i in range(n):
        if seen[i]: continue
        comps += 1; stack = [i]; seen[i] = True
        while stack:
            u = stack.pop()
            for v in range(n):
                if not seen[v] and set(otps[u]) & set(otps[v]):
                    seen[v] = True; stack.append(v)
    return comps
for _ in range(300):
    n = random.randint(1, 7)
    otps = [''.join(random.choice('abcdef') for _ in range(random.randint(1, 3))) for _ in range(n)]
    assert min_otps(n, otps) == brute(otps), otps
print('ok')

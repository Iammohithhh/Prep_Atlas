def find_minimum_idleness(shader, switch_count):
    n = len(shader)
    runs = []
    i = 0
    while i < n:
        j = i
        while j < n and shader[j] == shader[i]:
            j += 1
        runs.append(j - i)
        i = j

    def flips_needed(limit):
        if limit == 1:                                # alternate: compare with "abab..." and "baba..."
            p1 = sum(1 for k, ch in enumerate(shader) if ch != "ab"[k % 2])
            return min(p1, n - p1)
        return sum(r // (limit + 1) for r in runs)    # every (limit+1)-th character of a run must be flipped

    lo, hi = 1, max(runs)
    while lo < hi:
        mid = (lo + hi) // 2
        if flips_needed(mid) <= switch_count:
            hi = mid
        else:
            lo = mid + 1
    return lo

# ---- tests
import random
assert find_minimum_idleness("aabbbaaaa", 2) == 2
assert find_minimum_idleness("aaaaa", 1) == 2
assert find_minimum_idleness("ab", 0) == 1
def idle(s):
    best = cur = 1
    for a, b in zip(s, s[1:]):
        cur = cur + 1 if a == b else 1
        best = max(best, cur)
    return best
def brute(s, k):
    n = len(s); best = n
    for mask in range(1 << n):
        if bin(mask).count('1') > k: continue
        t = ''.join(('b' if c == 'a' else 'a') if mask >> i & 1 else c for i, c in enumerate(s))
        best = min(best, idle(t))
    return best
for _ in range(400):
    s = ''.join(random.choice('ab') for _ in range(random.randint(1, 10))); k = random.randint(0, len(s))
    assert find_minimum_idleness(s, k) == brute(s, k), (s, k)
print('ok')

def longest_same_segment(s, k):
    best = 0
    for ch in set(s):                       # fix the target type
        left = bad = 0
        for right, c in enumerate(s):
            if c != ch:
                bad += 1
            while bad > k:
                if s[left] != ch:
                    bad -= 1
                left += 1
            best = max(best, right - left + 1)
    return best

# ---- tests
import random
assert longest_same_segment("abaab", 1) == 4
def brute(s, k):
    n = len(s); best = 0
    for i in range(n):
        for j in range(i, n):
            seg = s[i:j + 1]
            if len(seg) - max(seg.count(c) for c in set(seg)) <= k:
                best = max(best, len(seg))
    return best
for _ in range(300):
    s = ''.join(random.choice('abc') for _ in range(random.randint(1, 9)))
    k = random.randint(0, 4)
    assert longest_same_segment(s, k) == brute(s, k)
print('ok')

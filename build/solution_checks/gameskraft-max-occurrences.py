from collections import Counter


def get_max_occurrences(components, min_length, max_length, max_unique):
    # Any valid longer substring contains a valid substring of length min_length that occurs at least as often,
    # so only windows of exactly min_length matter.
    if min_length > max_length:
        return 0
    s = components
    counts = Counter()
    freq = Counter()
    unique = 0
    for i, ch in enumerate(s):
        freq[ch] += 1
        if freq[ch] == 1:
            unique += 1
        if i >= min_length:
            old = s[i - min_length]
            freq[old] -= 1
            if freq[old] == 0:
                unique -= 1
        if i >= min_length - 1 and unique <= max_unique:
            counts[s[i - min_length + 1:i + 1]] += 1
    return max(counts.values(), default=0)

# ---- tests
import random
assert get_max_occurrences("abcde", 2, 4, 26) == 1
assert get_max_occurrences("ababab", 2, 3, 4) == 3
def brute(s, lo, hi, mu):
    cnt = Counter()
    for i in range(len(s)):
        for j in range(i + lo, min(len(s), i + hi) + 1):
            sub = s[i:j]
            if len(set(sub)) <= mu: cnt[sub] += 1
    return max(cnt.values(), default=0)
for _ in range(500):
    s = ''.join(random.choice('abc') for _ in range(random.randint(2, 14)))
    lo = random.randint(2, 4); hi = random.randint(lo, 5); mu = random.randint(2, 3)
    assert get_max_occurrences(s, lo, hi, mu) == brute(s, lo, hi, mu), (s, lo, hi, mu)
print('ok')

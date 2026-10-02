from collections import Counter


def get_lex_smallest_string(n, data):
    need = Counter(data)
    if len(need) > n:
        return "-1"

    def slots(k):                              # copies of s needed per letter, summed
        return sum(-(-c // k) for c in need.values())

    lo, hi = 1, max(need.values())             # at k = max(need) every letter needs one slot
    while lo < hi:
        mid = (lo + hi) // 2
        if slots(mid) <= n:
            hi = mid
        else:
            lo = mid + 1
    k = lo
    letters = []
    for ch, c in need.items():
        letters.extend(ch * (-(-c // k)))
    letters.extend('a' * (n - len(letters)))   # spare positions: the smallest letter
    return ''.join(sorted(letters))

# ---- tests
import random
from itertools import product
assert get_lex_smallest_string(2, "aavvavv") == "av"
assert get_lex_smallest_string(3, "aabaabba") == "aab"
assert get_lex_smallest_string(4, "abacbca") == "aabc"
assert get_lex_smallest_string(1, "ab") == "-1"
def brute(n, data):
    need = Counter(data)
    best = None
    for s in product('abcd', repeat=n):
        m = Counter(s)
        if any(m[c] == 0 for c in need): continue
        k = max(-(-need[c] // m[c]) for c in need)
        key = (k, ''.join(s))
        if best is None or key < best: best = key
    return best[1] if best else "-1"
for _ in range(300):
    n = random.randint(1, 5)
    data = ''.join(random.choice('abcd') for _ in range(random.randint(1, 12)))
    assert get_lex_smallest_string(n, data) == brute(n, data), (n, data)
print('ok')

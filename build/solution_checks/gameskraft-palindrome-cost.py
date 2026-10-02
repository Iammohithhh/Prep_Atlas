def get_total_palindrome_transformation_cost(dna):
    n = len(dna)
    mask = 0
    ones = [0] * 26                  # number of prefixes whose parity bit b is 1
    for ch in dna:
        mask ^= 1 << (ord(ch) - 97)
        for b in range(26):
            ones[b] += (mask >> b) & 1
    prefixes = n + 1                 # includes the empty prefix (mask 0)
    sum_popcount = sum(c * (prefixes - c) for c in ones)   # total over pairs of popcount(prefix_i xor prefix_j)
    even = (prefixes + 1) // 2       # prefix indices 0, 2, 4, ...
    odd = prefixes // 2
    odd_length_pairs = even * odd    # popcount parity equals substring-length parity
    return (sum_popcount - odd_length_pairs) // 2

# ---- tests
import random
assert get_total_palindrome_transformation_cost("abca") == 6
def cost(sub):
    from collections import Counter
    return sum(1 for v in Counter(sub).values() if v % 2) // 2
def brute(s):
    return sum(cost(s[i:j]) for i in range(len(s)) for j in range(i + 1, len(s) + 1))
for _ in range(500):
    s = ''.join(random.choice('abcde') for _ in range(random.randint(1, 15)))
    assert get_total_palindrome_transformation_cost(s) == brute(s), s
get_total_palindrome_transformation_cost('ab' * 100000)
print('ok')

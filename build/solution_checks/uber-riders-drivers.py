def assign(n, a):
    """Alternating assignment; returns an empty string when n is odd (equal counts impossible)."""
    if n % 2:
        return ''
    even = sum(a[0::2])
    odd = sum(a[1::2])
    # riders on even indices -> "RDRD..."; riders on odd indices -> "DRDR..."
    if even > odd:
        return 'RD' * (n // 2)
    return 'DR' * (n // 2)       # odd >= even; on a tie "DR.." is lexicographically smaller

# ---- tests
import random
from itertools import product
assert assign(4, [1, 2, 3, 4]) == 'DRDR'
assert assign(4, [5, 1, 5, 1]) == 'RDRD'
assert assign(3, [1, 2, 3]) == ''
for _ in range(300):
    n = random.choice([2, 4, 6, 8]); a = [random.randint(1, 9) for _ in range(n)]
    best = None
    for s in product('DR', repeat=n):
        s = ''.join(s)
        if s.count('R') != s.count('D'): continue
        if any(s[i] == s[i + 1] for i in range(n - 1)): continue
        v = sum(a[i] for i in range(n) if s[i] == 'R') - sum(a[i] for i in range(n) if s[i] == 'D')
        if best is None or v > best[0] or (v == best[0] and s < best[1]): best = (v, s)
    assert assign(n, a) == best[1]
print('ok')

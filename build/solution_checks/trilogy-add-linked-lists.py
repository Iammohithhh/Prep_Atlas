BASE = 10000


def add_chunks(a, b):
    """a, b: lists of 4-digit chunks (most significant first, first chunk has no leading zeros)."""
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    out = []
    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += a[i]
            i -= 1
        if j >= 0:
            total += b[j]
            j -= 1
        out.append(total % BASE)
        carry = total // BASE
    out.reverse()
    return out or [0]

# ---- tests
import random
assert add_chunks([9876, 5432, 1999], [1, 8001]) == [9876, 5434, 0]
assert add_chunks([123, 4, 5], [100, 100, 100]) == [223, 104, 105]
assert add_chunks([9999], [1]) == [1, 0]
assert add_chunks([], []) == [0]
def val(ch):
    v = 0
    for x in ch: v = v * BASE + x
    return v
def mk(n):
    ch = []
    while n: ch.append(n % BASE); n //= BASE
    return ch[::-1]
for _ in range(500):
    x, y = random.randint(0, 10**random.randint(0, 20)), random.randint(0, 10**random.randint(0, 20))
    assert val(add_chunks(mk(x), mk(y))) == x + y
print('ok')

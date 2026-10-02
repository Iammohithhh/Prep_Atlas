def prefixes_div_by_5(codes):
    out = []
    rem = 0
    for bit in codes:
        rem = (rem * 2 + bit) % 5      # keep only the remainder
        out.append(rem == 0)
    return out

# ---- tests
import random
assert prefixes_div_by_5([1, 0, 1]) == [False, False, True]
for _ in range(200):
    a = [random.randint(0, 1) for _ in range(random.randint(1, 20))]
    exp = [int(''.join(map(str, a[:i + 1])), 2) % 5 == 0 for i in range(len(a))]
    assert prefixes_div_by_5(a) == exp
print('ok')

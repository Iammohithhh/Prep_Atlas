def count_power_numbers(l, r):
    powers = {0}
    if r >= 1:
        powers.add(1)
    b = 2
    while b * b <= r:
        v = b * b
        while v <= r:
            powers.add(v)
            v *= b
        b += 1
    P = sorted(powers)
    hit = bytearray(r + 1)
    for i, x in enumerate(P):
        for j in range(i, len(P)):
            s = x + P[j]
            if s > r:
                break
            hit[s] = 1
    return sum(hit[l:r + 1])

# ---- tests
assert count_power_numbers(20, 25) == 3
assert count_power_numbers(0, 0) == 1
def brute(l, r):
    pw = set()
    for a in range(0, r + 1):
        for p in range(2, 25):
            if a ** p <= r:
                pw.add(a ** p)
    return len({x for x in range(l, r + 1) if any(x - y in pw for y in pw)})
for l, r in [(0, 100), (5, 60), (0, 300), (37, 200), (1, 1), (0, 1)]:
    assert count_power_numbers(l, r) == brute(l, r), (l, r)
print('ok')

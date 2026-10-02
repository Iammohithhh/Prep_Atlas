def count_numbers(arr):
    top = max(m for _, m in arr)
    prefix = [0] * (top + 1)
    for x in range(1, top + 1):
        seen = 0
        ok = 1
        y = x
        while y:
            bit = 1 << (y % 10)
            if seen & bit:
                ok = 0
                break
            seen |= bit
            y //= 10
        prefix[x] = prefix[x - 1] + ok
    return [prefix[m] - prefix[n - 1] for n, m in arr]

# ---- tests
import random
assert count_numbers([[80, 120]]) == [27]
for _ in range(100):
    qs = []
    for _ in range(5):
        a = random.randint(1, 3000); b = random.randint(a, 3000)
        qs.append([a, b])
    exp = [sum(1 for v in range(a, b + 1) if len(set(str(v))) == len(str(v))) for a, b in qs]
    assert count_numbers(qs) == exp
print('ok')

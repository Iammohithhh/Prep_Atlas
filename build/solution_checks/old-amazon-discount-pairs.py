def find_pairs(x, cost):
    seen = {}
    total = 0
    for c in cost:
        r = c % x
        total += seen.get((-r) % x, 0)
        seen[r] = seen.get(r, 0) + 1
    return total

# ---- tests
import random
assert find_pairs(60, [31, 25, 85, 29, 35]) == 3
assert find_pairs(10, [3, 7, 27, 23]) == 4
for _ in range(300):
    c = [random.randint(1, 30) for _ in range(random.randint(1, 10))]; x = random.randint(1, 12)
    assert find_pairs(x, c) == sum(1 for i in range(len(c)) for j in range(i + 1, len(c)) if (c[i] + c[j]) % x == 0)
print('ok')

from collections import defaultdict


def divisible_pairs(values, k):
    seen = defaultdict(int)
    total = 0
    for v in values:
        r = v % k                             # Python keeps the remainder in [0, k) for negatives too
        total += seen[(-r) % k]              # earlier elements that complete the pair (query before updating)
        seen[r] += 1
    return total

# ---- tests
import random
assert divisible_pairs([1, 2, 3, 4, 5], 3) == 4
assert divisible_pairs([-1, 1, 2, -2], 3) == 4
assert divisible_pairs([5, 5], 5) == 1
def brute(v, k):
    return sum(1 for i in range(len(v)) for j in range(i + 1, len(v)) if (v[i] + v[j]) % k == 0)
for _ in range(400):
    k = random.randint(1, 7)
    v = [random.randint(-12, 12) for _ in range(random.randint(0, 12))]
    assert divisible_pairs(v, k) == brute(v, k)
print('ok')

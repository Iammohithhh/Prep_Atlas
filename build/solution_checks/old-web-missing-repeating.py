def find_missing_and_repeating(a):
    n = len(a)
    s1 = sum(a) - n * (n + 1) // 2                      # repeating - missing
    s2 = sum(x * x for x in a) - n * (n + 1) * (2 * n + 1) // 6   # repeating^2 - missing^2
    total = s2 // s1                                     # repeating + missing
    repeating = (total + s1) // 2
    return repeating, repeating - s1

# ---- tests
import random
assert find_missing_and_repeating([3, 1, 3]) == (3, 2)
assert find_missing_and_repeating([4, 3, 6, 2, 1, 1]) == (1, 5)
for _ in range(400):
    n = random.randint(2, 12)
    a = list(range(1, n + 1))
    missing = random.choice(a)
    rep = random.choice([x for x in a if x != missing])
    a[a.index(missing)] = rep
    random.shuffle(a)
    assert find_missing_and_repeating(a) == (rep, missing)
print('ok')

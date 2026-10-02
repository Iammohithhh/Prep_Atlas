def solve(m, s):
    odd_strings = 0
    for word in s:
        if all(ord(ch) % 2 == 1 for ch in word):     # ord(c)**m has the parity of ord(c) for m >= 1
            odd_strings ^= 1
    return "ODD" if odd_strings else "EVEN"

# ---- tests
import random
assert solve(2, ["abc", "abcd"]) == "EVEN"
assert solve(47, ["azbde", "abcher", "acegk"]) == "ODD"
def brute(m, s):
    total = 0
    for word in s:
        p = 1
        for ch in word:
            p *= ord(ch) ** m
        total += p
    return "ODD" if total % 2 else "EVEN"
for _ in range(300):
    m = random.randint(1, 4)
    s = [''.join(random.choice('acegbdz') for _ in range(random.randint(1, 4))) for _ in range(random.randint(2, 5))]
    assert solve(m, s) == brute(m, s)
print('ok')

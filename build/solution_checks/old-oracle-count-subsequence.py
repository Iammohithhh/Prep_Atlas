def get_subsequence_count(s1, s2):
    c1 = c2 = c3 = 0
    for ch in s2:
        if ch == s1[2]:
            c3 += c2
        if ch == s1[1]:
            c2 += c1
        if ch == s1[0]:
            c1 += 1
    return c3

# ---- tests
import random
assert get_subsequence_count("ABC", "ABCBABC") == 5
assert get_subsequence_count("HRW", "HERHRWS") == 3
for _ in range(300):
    s1 = ''.join(random.choice('AB') for _ in range(3)); s2 = ''.join(random.choice('AB') for _ in range(random.randint(0, 10)))
    n = len(s2)
    exp = sum(1 for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n) if s2[i] + s2[j] + s2[k] == s1)
    assert get_subsequence_count(s1, s2) == exp
print('ok')

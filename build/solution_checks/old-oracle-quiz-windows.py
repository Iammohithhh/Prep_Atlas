def team_size(talent, talents_count):
    n = len(talent)
    freq = [0] * (talents_count + 1)
    distinct = 0
    out = [-1] * n
    right = 0                                         # window is talent[left:right]
    for left in range(n):
        while right < n and distinct < talents_count:
            if freq[talent[right]] == 0:
                distinct += 1
            freq[talent[right]] += 1
            right += 1
        if distinct == talents_count:
            out[left] = right - left
        freq[talent[left]] -= 1
        if freq[talent[left]] == 0:
            distinct -= 1
    return out

# ---- tests
import random
assert team_size([1, 2, 3, 2, 1], 3) == [3, 4, 3, -1, -1]
assert team_size([1, 1, 2, 2, 3, 1, 3, 2], 3) == [5, 4, 4, 3, 4, 3, -1, -1]
for _ in range(300):
    c = random.randint(1, 4); t = [random.randint(1, c) for _ in range(random.randint(1, 10))]
    exp = []
    for i in range(len(t)):
        res = -1
        for j in range(i, len(t)):
            if len(set(t[i:j + 1])) == c: res = j - i + 1; break
        exp.append(res)
    assert team_size(t, c) == exp
print('ok')

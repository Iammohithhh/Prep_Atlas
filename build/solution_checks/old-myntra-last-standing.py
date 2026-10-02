def last_standing(s, k):
    length = len(s)
    head, step, count = 1, 1, length * k             # surviving positions: head, head+step, ... (1-indexed)
    left_to_right = True
    while count > 1:
        if left_to_right:
            head += step                              # the first element is removed
        else:
            if count % 2 == 1:                        # the last one is removed first, so the first survives only when count is even
                head += step
        count //= 2
        step *= 2
        left_to_right = not left_to_right
    return s[(head - 1) % length]

# ---- tests
import random
def brute(s, k):
    t = list(s * k); ltr = True
    while len(t) > 1:
        if ltr: t = t[1::2]
        else: t = t[::-1][1::2][::-1]
        ltr = not ltr
    return t[0]
assert last_standing("abcd", 3) == "b"
assert last_standing("j#k&h", 5) == "&"
for _ in range(500):
    s = ''.join(random.choice('abcdef') for _ in range(random.randint(1, 6))); k = random.randint(1, 6)
    assert last_standing(s, k) == brute(s, k), (s, k)
print('ok')

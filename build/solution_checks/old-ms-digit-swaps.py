def min_swaps(S, T):
    n = len(S)
    first = None
    for i in range(n):
        if S[i] != T[i]:
            first = i
            break
    if first is None:
        return 0
    # orientation A: keep the first unequal pair (S gets the larger digit there); orientation B: swap it
    def cost(first_swapped):
        swaps = 1 if first_swapped else 0
        a_bigger = (S[first] > T[first]) != first_swapped      # is the first number larger after the decision at `first`?
        for i in range(first + 1, n):
            if S[i] == T[i]:
                continue
            hi, lo = max(S[i], T[i]), min(S[i], T[i])
            # the larger number should receive the smaller digit, the smaller number the larger digit
            first_gets_hi = (S[i] == hi)
            wants_first_hi = not a_bigger                      # S-number (first string) is the smaller number if a_bigger is False
            if first_gets_hi != wants_first_hi:
                swaps += 1
        return swaps
    return min(cost(False), cost(True))

# ---- tests
import random
assert min_swaps("29162", "10524") == 2
def brute(S, T):
    n = len(S); best = None
    for mask in range(1 << n):
        a = ''.join(T[i] if mask >> i & 1 else S[i] for i in range(n))
        b = ''.join(S[i] if mask >> i & 1 else T[i] for i in range(n))
        if a[0] == '0' or b[0] == '0': continue
        key = (abs(int(a) - int(b)), bin(mask).count('1'))
        if best is None or key < best: best = key
    return best[1] if best else None
for _ in range(500):
    n = random.randint(1, 7)
    S = str(random.randint(1, 9)) + ''.join(random.choice('0123456789') for _ in range(n - 1))
    T = str(random.randint(1, 9)) + ''.join(random.choice('0123456789') for _ in range(n - 1))
    b = brute(S, T)
    if b is None: continue
    assert min_swaps(S, T) == b, (S, T)
print('ok')

def count_solutions(crypt):
    w1, w2, w3 = [w[::-1] for w in crypt]          # least significant digit first
    letters = set(crypt[0] + crypt[1] + crypt[2])
    if len(letters) > 10:
        return 0
    leading = {w[0] for w in crypt if len(w) > 1}
    length = max(len(w1), len(w2), len(w3))
    assign = {}
    used = [False] * 10

    def digit_options(ch):
        if ch in assign:
            return [assign[ch]]
        return [d for d in range(10) if not used[d] and not (d == 0 and ch in leading)]

    def solve_col(col, carry):
        if col == length:
            return 1 if carry == 0 else 0
        cols = [w[col] if col < len(w) else None for w in (w1, w2, w3)]
        new = []                                     # letters first met in this column
        for ch in cols:
            if ch is not None and ch not in assign and ch not in new:
                new.append(ch)
        return assign_letters(col, carry, cols, new, 0)

    def assign_letters(col, carry, cols, new, idx):
        if idx == len(new):
            x, y, z = (assign[ch] if ch is not None else 0 for ch in cols)
            total = x + y + carry
            if total % 10 != z:
                return 0
            return solve_col(col + 1, total // 10)
        ch = new[idx]
        count = 0
        for d in digit_options(ch):
            assign[ch] = d
            used[d] = True
            count += assign_letters(col, carry, cols, new, idx + 1)
            used[d] = False
            del assign[ch]
        return count

    return solve_col(0, 0)

# ---- tests
import random
from itertools import permutations
assert count_solutions(["SEND", "MORE", "MONEY"]) == 1
assert count_solutions(["GREEN", "BLUE", "BLACK"]) == 12
assert count_solutions(["ONE", "TWO", "THREE"]) == 0
def brute(crypt):
    letters = sorted(set(''.join(crypt)))
    if len(letters) > 10: return 0
    cnt = 0
    for p in permutations(range(10), len(letters)):
        mp = dict(zip(letters, p))
        if any(len(w) > 1 and mp[w[0]] == 0 for w in crypt): continue
        v = [int(''.join(str(mp[ch]) for ch in w)) for w in crypt]
        if v[0] + v[1] == v[2]: cnt += 1
    return cnt
for _ in range(25):
    pool = 'ABCDE'
    crypt = [''.join(random.choice(pool) for _ in range(random.randint(1, 3))) for _ in range(3)]
    assert count_solutions(crypt) == brute(crypt), crypt
print('ok')

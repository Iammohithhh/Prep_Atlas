def find_capable_winners(a_list, b_list, c_list):
    n = len(a_list)
    trips = [tuple(sorted(t)) for t in zip(a_list, b_list, c_list)]
    # X beats Y iff b_X > a_Y and c_X > b_Y (X's two largest boosters against Y's two smallest)
    # player i qualifies iff for every other player j: b_i > a_j and c_i > b_j
    def top2(vals):
        first = second = (-1, -1)
        for idx, v in enumerate(vals):
            if v > first[0]:
                first, second = (v, idx), first
            elif v > second[0]:
                second = (v, idx)
        return first, second
    ta = top2([t[0] for t in trips])
    tb = top2([t[1] for t in trips])
    count = 0
    for i, (a, b, c) in enumerate(trips):
        max_a_other = ta[0][0] if ta[0][1] != i else ta[1][0]
        max_b_other = tb[0][0] if tb[0][1] != i else tb[1][0]
        if b > max_a_other and c > max_b_other:
            count += 1
    return count

# ---- tests
import random
from itertools import permutations
assert find_capable_winners([9, 4, 2], [5, 12, 10], [11, 3, 13]) == 2
assert find_capable_winners([4, 2], [8, 5], [10, 12]) == 2
def beats(x, y):
    for px in permutations(x):
        for py in permutations(y):
            if sum(1 for p, q in zip(px, py) if p > q) >= 2: return True
    return False
def brute(a, b, c):
    n = len(a); t = list(zip(a, b, c)); cnt = 0
    for i in range(n):
        if all(beats(t[i], t[j]) for j in range(n) if j != i): cnt += 1
    return cnt
for _ in range(400):
    n = random.randint(2, 5)
    trip = [random.sample(range(1, 15), 3) for _ in range(n)]
    a, b, c = [t[0] for t in trip], [t[1] for t in trip], [t[2] for t in trip]
    assert find_capable_winners(a, b, c) == brute(a, b, c), (a, b, c)
print('ok')

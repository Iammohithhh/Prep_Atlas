def max_supplies(credits, costs):
    count = 0
    for c in sorted(costs):
        if credits < c:
            break
        credits -= c
        count += 1
    return count

# ---- tests
import random
assert max_supplies(7, [1, 3, 2, 4, 1]) == 4
for _ in range(300):
    costs = [random.randint(1, 9) for _ in range(random.randint(1, 8))]; cr = random.randint(0, 30)
    best = 0
    for mask in range(1 << len(costs)):
        s = sum(costs[i] for i in range(len(costs)) if mask >> i & 1)
        if s <= cr: best = max(best, bin(mask).count('1'))
    assert max_supplies(cr, costs) == best
print('ok')

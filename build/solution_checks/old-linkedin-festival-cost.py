def minimize_cost(num_people, x, y):
    def median(coords):
        pairs = sorted(zip(coords, num_people))
        total = sum(num_people)
        run = 0
        for c, w in pairs:
            run += w
            if 2 * run >= total:
                return c
    a, b = median(x), median(y)
    return sum(w * (abs(xi - a) + abs(yi - b)) for w, xi, yi in zip(num_people, x, y))

# ---- tests
import random
assert minimize_cost([1, 2], [1, 3], [1, 3]) == 4
assert minimize_cost([1, 1], [1, 3], [1, 1]) == 2
def brute(w, x, y):
    return min(sum(wi * (abs(xi - a) + abs(yi - b)) for wi, xi, yi in zip(w, x, y))
               for a in range(0, 12) for b in range(0, 12))
for _ in range(300):
    n = random.randint(1, 6)
    w = [random.randint(1, 5) for _ in range(n)]
    x = [random.randint(1, 9) for _ in range(n)]
    y = [random.randint(1, 9) for _ in range(n)]
    assert minimize_cost(w, x, y) == brute(w, x, y)
print('ok')

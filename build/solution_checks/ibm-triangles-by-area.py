from math import sqrt


def sort_by_area(triangles):
    def area(t):
        a, b, c = t
        p = (a + b + c) / 2
        return sqrt(p * (p - a) * (p - b) * (p - c))
    # compare 16·area² = (a+b+c)(-a+b+c)(a-b+c)(a+b-c) exactly with integers
    def key(t):
        a, b, c = t
        return (a + b + c) * (-a + b + c) * (a - b + c) * (a + b - c)
    return sorted(triangles, key=key)

# ---- tests
assert sort_by_area([(7, 24, 25), (5, 12, 13), (3, 4, 5)]) == [(3, 4, 5), (5, 12, 13), (7, 24, 25)]
import random
for _ in range(200):
    ts = []
    while len(ts) < 5:
        a, b, c = random.randint(1, 70), random.randint(1, 70), random.randint(1, 70)
        if a + b > c and a + c > b and b + c > a: ts.append((a, b, c))
    r = sort_by_area(ts)
    areas = [sqrt((sum(t) / 2) * (sum(t) / 2 - t[0]) * (sum(t) / 2 - t[1]) * (sum(t) / 2 - t[2])) for t in r]
    assert all(x <= y + 1e-9 for x, y in zip(areas, areas[1:]))
print('ok')

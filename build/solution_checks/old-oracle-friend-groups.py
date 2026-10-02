def get_the_groups(n, query_type, students1, students2):
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    out = []
    for q, a, b in zip(query_type, students1, students2):
        ra, rb = find(a), find(b)
        if q == 'Friend':
            if ra != rb:
                if size[ra] < size[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                size[ra] += size[rb]
        else:                                          # Total: sizes of the two groups added (counted twice when they coincide)
            out.append(size[ra] + size[rb])
    return out

# ---- tests
import random
assert get_the_groups(4, ["Friend", "Friend", "Total"], [1, 2, 1], [2, 3, 4]) == [4]
for _ in range(300):
    n = random.randint(2, 7); q = random.randint(1, 10)
    qt = [random.choice(['Friend', 'Total']) for _ in range(q)]
    a = [random.randint(1, n) for _ in range(q)]; b = [random.randint(1, n) for _ in range(q)]
    groups = [{i} for i in range(n + 1)]
    exp = []
    for t, x, y in zip(qt, a, b):
        gx = next(g for g in groups if x in g); gy = next(g for g in groups if y in g)
        if t == 'Friend':
            if gx is not gy: gx |= gy; groups.remove(gy)
        else: exp.append(len(gx) + len(gy))
    assert get_the_groups(n, qt, a, b) == exp
print('ok')

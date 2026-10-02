def min_cost(n, c_link, c_service, pairs):
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for u, v in pairs:
        ru, rv = find(u), find(v)
        if ru != rv:
            if size[ru] < size[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            size[ru] += size[rv]
    total = 0
    for v in range(1, n + 1):
        if find(v) == v:
            s = size[v]
            # host in every cluster, or host once and connect the other s-1 clusters with a spanning tree
            total += min(s * c_service, c_service + (s - 1) * c_link)
    return total

# ---- tests
assert min_cost(5, 1, 3, [(1, 2), (1, 3), (3, 2), (4, 5)]) == 9
assert min_cost(3, 10, 1, []) == 3
print('ok')

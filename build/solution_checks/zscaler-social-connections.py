def get_visible_profiles_count(connection_nodes, connection_from, connection_to, queries):
    parent = list(range(connection_nodes + 1))
    size = [1] * (connection_nodes + 1)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for u, v in zip(connection_from, connection_to):
        ru, rv = find(u), find(v)
        if ru != rv:
            if size[ru] < size[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            size[ru] += size[rv]
    return [size[find(q)] for q in queries]

# ---- tests
assert get_visible_profiles_count(5, [2, 2, 1, 1], [1, 3, 3, 4], [4, 2, 5]) == [4, 4, 1]
assert get_visible_profiles_count(7, [1, 2, 3, 5], [2, 3, 4, 6], [1, 3, 5, 7]) == [4, 4, 2, 1]
print('ok')

def digit_sum(v):
    return sum(int(c) for c in str(abs(v)))


def supernode_sum(root_value, nodes):
    """nodes: dict mapping a path such as 'L', 'RR', 'RRL' to its value; the root is the empty path."""
    values = dict(nodes)
    values[''] = root_value
    total = 0
    for path, v in values.items():
        left, right = path + 'L', path + 'R'
        if left in values and right in values and digit_sum(values[left]) == digit_sum(values[right]):
            total += v
    return total

# ---- tests
def parse(text):
    lines = text.split('\n')
    n = int(lines[0]); root = int(lines[1])
    nodes = {}
    for ln in lines[2:2 + n - 1]:
        p, v = ln.split()
        nodes[p] = int(v)
    return root, nodes
assert supernode_sum(*parse("8\n21\nL 14\nR 23\nLL 7\nLR 70\nRR 11\nRRL 23\nRRR 32")) == 46
assert supernode_sum(*parse("6\n11\nL 14\nR 23\nLL 7\nLR 8\nRR 14")) == 11
assert supernode_sum(5, {}) == 0
assert supernode_sum(5, {'L': 12, 'R': 21}) == 5
print('ok')

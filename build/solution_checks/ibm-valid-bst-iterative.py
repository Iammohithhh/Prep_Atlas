def is_valid_bst(root):
    """root: level-order list of strings with "null" for missing children (as in the problem input)."""
    if not root or root[0] == "null":
        return True
    # build the tree without recursion
    vals = [None if x == "null" else int(x) for x in root]
    left = {}
    right = {}
    queue = [0]                                  # indices into `vals` used as node ids
    nxt = 1
    qi = 0
    while qi < len(queue) and nxt < len(vals):
        node = queue[qi]; qi += 1
        if nxt < len(vals) and vals[nxt] is not None:
            left[node] = nxt; queue.append(nxt)
        nxt += 1
        if nxt < len(vals) and vals[nxt] is not None:
            right[node] = nxt; queue.append(nxt)
        nxt += 1
    # iterative in-order traversal: values must be strictly increasing
    stack = []
    cur = 0
    prev = None
    while cur is not None or stack:
        while cur is not None:
            stack.append(cur)
            cur = left.get(cur)
        cur = stack.pop()
        if prev is not None and vals[cur] <= prev:
            return False
        prev = vals[cur]
        cur = right.get(cur)
    return True

# ---- tests
import random
assert is_valid_bst(["2", "1", "3"]) is True
assert is_valid_bst(["5", "1", "4", "null", "null", "3", "6"]) is False
assert is_valid_bst(["1", "1"]) is False
assert is_valid_bst(["null"]) is True
def build(root):
    vals = [None if x == "null" else int(x) for x in root]
    class N:
        def __init__(s, v): s.v = v; s.l = s.r = None
    nodes = {0: N(vals[0])}; q = [0]; nxt = 1; qi = 0
    while qi < len(q) and nxt < len(vals):
        u = q[qi]; qi += 1
        if nxt < len(vals) and vals[nxt] is not None: nodes[nxt] = N(vals[nxt]); nodes[u].l = nodes[nxt]; q.append(nxt)
        nxt += 1
        if nxt < len(vals) and vals[nxt] is not None: nodes[nxt] = N(vals[nxt]); nodes[u].r = nodes[nxt]; q.append(nxt)
        nxt += 1
    return nodes[0]
def rec(n, lo=float('-inf'), hi=float('inf')):
    return True if n is None else lo < n.v < hi and rec(n.l, lo, n.v) and rec(n.r, n.v, hi)
for _ in range(500):
    size = random.randint(1, 9)
    arr = [str(random.randint(1, 9))] + [random.choice(["null", str(random.randint(1, 9))]) for _ in range(size - 1)]
    assert is_valid_bst(arr) == rec(build(arr)), arr
print('ok')

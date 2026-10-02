class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build(level):
    if not level or level[0] is None:
        return None
    nodes = [None if v is None else TreeNode(v) for v in level]
    kids = iter(nodes[1:])
    for node in nodes:
        if node is not None:
            node.left = next(kids, None)
            node.right = next(kids, None)
    return nodes[0]


def left_view(root):
    view, level = [], [root] if root else []
    while level:
        view.append(level[0].val)             # first node of every level
        level = [c for node in level for c in (node.left, node.right) if c]
    return view


def is_sum_tree(root):
    def go(node):                              # returns (is_sum_tree, sum of the subtree)
        if node is None:
            return True, 0
        if node.left is None and node.right is None:
            return True, node.val
        lo, ls = go(node.left)
        ro, rs = go(node.right)
        return lo and ro and node.val == ls + rs, node.val + ls + rs
    return go(root)[0]


def count_left_sum_exceeds(root, threshold):
    count = 0
    def total(node):
        nonlocal count
        if node is None:
            return 0
        ls = total(node.left)
        rs = total(node.right)
        if ls > threshold:
            count += 1
        return ls + rs + node.val
    total(root)
    return count

# ---- tests
import random
t = build([10, 20, 30, 40, 60])
assert left_view(t) == [10, 20, 40]
assert is_sum_tree(build([26, 10, 3, 4, 6, None, 3]))
assert not is_sum_tree(build([10, 20, 30]))
assert count_left_sum_exceeds(build([1, 5, 2, 4]), 3) == 2
def rand_tree(n):
    if n == 0:
        return None
    root = TreeNode(random.randint(1, 9))
    free = [(root, 'left'), (root, 'right')]
    for _ in range(n - 1):
        node, side = free.pop(random.randrange(len(free)))
        child = TreeNode(random.randint(1, 9))
        setattr(node, side, child)
        free += [(child, 'left'), (child, 'right')]
    return root
def subtree_sum(x):
    return 0 if x is None else x.val + subtree_sum(x.left) + subtree_sum(x.right)
def nodes_of(x):
    return [] if x is None else [x] + nodes_of(x.left) + nodes_of(x.right)
def brute_left_view(root):
    best = {}
    def walk(x, d, path):
        if x is None:
            return
        key = (d, path)
        best.setdefault(d, []).append((path, x.val))
        walk(x.left, d + 1, path + '0'); walk(x.right, d + 1, path + '1')
    walk(root, 0, '')
    return [min(best[d])[1] for d in sorted(best)]
def brute_sum_tree(root):
    return all(x.val == subtree_sum(x.left) + subtree_sum(x.right) for x in nodes_of(root) if x.left or x.right)
for _ in range(300):
    tr = rand_tree(random.randint(1, 9))
    assert left_view(tr) == brute_left_view(tr)
    assert is_sum_tree(tr) == brute_sum_tree(tr)
    th = random.randint(0, 12)
    assert count_left_sum_exceeds(tr, th) == sum(1 for x in nodes_of(tr) if subtree_sum(x.left) > th)
print('ok')

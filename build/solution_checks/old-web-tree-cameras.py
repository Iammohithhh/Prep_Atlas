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


def min_camera_cover(root):
    cams = 0
    # state: 0 = not covered, 1 = covered without camera, 2 = has a camera
    def dfs(node):
        nonlocal cams
        if node is None:
            return 1
        l, r = dfs(node.left), dfs(node.right)
        if l == 0 or r == 0:
            cams += 1
            return 2
        if l == 2 or r == 2:
            return 1
        return 0
    if dfs(root) == 0:
        cams += 1
    return cams

# ---- tests
import random
assert min_camera_cover(build([0, 0, None, 0, 0])) == 1
assert min_camera_cover(build([0, 0, None, 0, None, 0, None, None, 0])) == 2
assert min_camera_cover(build([0])) == 1
def brute(root):
    nodes = []
    def walk(x, p):
        if x:
            nodes.append((x, p)); walk(x.left, x); walk(x.right, x)
    walk(root, None)
    best = len(nodes)
    for mask in range(1 << len(nodes)):
        chosen = {id(nodes[i][0]) for i in range(len(nodes)) if mask >> i & 1}
        ok = True
        for x, p in nodes:
            cover = id(x) in chosen or (p is not None and id(p) in chosen) or \
                    (x.left and id(x.left) in chosen) or (x.right and id(x.right) in chosen)
            if not cover:
                ok = False; break
        if ok:
            best = min(best, len(chosen))
    return best
def rand_tree(n):
    if n == 0:
        return None
    root = TreeNode(0)
    free = [(root, 'left'), (root, 'right')]
    for _ in range(n - 1):
        node, side = free.pop(random.randrange(len(free)))
        child = TreeNode(0)
        setattr(node, side, child)
        free += [(child, 'left'), (child, 'right')]
    return root
for _ in range(300):
    t = rand_tree(random.randint(1, 10))
    assert min_camera_cover(t) == brute(t)
print('ok')

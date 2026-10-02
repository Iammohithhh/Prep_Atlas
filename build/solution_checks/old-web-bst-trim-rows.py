class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def trim_bst(root, low, high):
    if root is None:
        return None
    if root.val < low:
        return trim_bst(root.right, low, high)    # the node and its left subtree are too small
    if root.val > high:
        return trim_bst(root.left, low, high)     # the node and its right subtree are too large
    root.left = trim_bst(root.left, low, high)
    root.right = trim_bst(root.right, low, high)
    return root


def sort_each_row(matrix):
    return [sorted(row) for row in matrix]


def sort_rows_lexicographically(matrix):
    return sorted(matrix)

# ---- tests
import random
def insert(root, v):
    if root is None:
        return TreeNode(v)
    if v < root.val:
        root.left = insert(root.left, v)
    else:
        root.right = insert(root.right, v)
    return root
def inorder(x):
    return inorder(x.left) + [x.val] + inorder(x.right) if x else []
def check_bst(x, lo=float('-inf'), hi=float('inf')):
    return x is None or (lo < x.val < hi and check_bst(x.left, lo, x.val) and check_bst(x.right, x.val, hi))
def parent_map(x, out=None, p=None):
    out = {} if out is None else out
    if x:
        out[x.val] = p
        parent_map(x.left, out, x.val); parent_map(x.right, out, x.val)
    return out
for _ in range(300):
    vals = random.sample(range(0, 30), random.randint(0, 12))
    root = None
    for v in vals:
        root = insert(root, v)
    lo = random.randint(0, 20); hi = lo + random.randint(0, 12)
    before = inorder(root)
    res = trim_bst(root, lo, hi)
    assert inorder(res) == [v for v in before if lo <= v <= hi]
    assert check_bst(res)
assert sort_each_row([[3, 1, 2], [9, 8]]) == [[1, 2, 3], [8, 9]]
assert sort_rows_lexicographically([[3, 1], [1, 5], [1, 2]]) == [[1, 2], [1, 5], [3, 1]]
print('ok')

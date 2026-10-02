class SegTree:
    """Stores bitwise AND and OR of each range, with lazy XOR."""

    def __init__(self, arr):
        n = len(arr)
        self.n = n
        self.an = [0] * (4 * n)
        self.orr = [0] * (4 * n)
        self.lz = [0] * (4 * n)
        self._build(1, 0, n - 1, arr)

    def _build(self, node, lo, hi, arr):
        if lo == hi:
            self.an[node] = self.orr[node] = arr[lo]
            return
        mid = (lo + hi) // 2
        self._build(2 * node, lo, mid, arr)
        self._build(2 * node + 1, mid + 1, hi, arr)
        self._pull(node)

    def _pull(self, node):
        self.an[node] = self.an[2 * node] & self.an[2 * node + 1]
        self.orr[node] = self.orr[2 * node] | self.orr[2 * node + 1]

    def _apply(self, node, z):
        a, o = self.an[node], self.orr[node]
        # XOR with z: bits where z=1 swap roles (AND becomes NOT OR, OR becomes NOT AND)
        self.an[node] = (a & ~z) | (~o & z)
        self.orr[node] = (o & ~z) | (~a & z)
        self.lz[node] ^= z

    def _push(self, node):
        if self.lz[node]:
            self._apply(2 * node, self.lz[node])
            self._apply(2 * node + 1, self.lz[node])
            self.lz[node] = 0

    def first_zero_bit(self, node, lo, hi, x, mask):
        """First index >= x whose value lacks `mask`; n if none."""
        if hi < x or self.an[node] & mask:
            return self.n
        if lo == hi:
            return lo
        self._push(node)
        mid = (lo + hi) // 2
        r = self.first_zero_bit(2 * node, lo, mid, x, mask)
        if r != self.n:
            return r
        return self.first_zero_bit(2 * node + 1, mid + 1, hi, x, mask)

    def xor_range(self, node, lo, hi, l, r, z):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            self._apply(node, z)
            return
        self._push(node)
        mid = (lo + hi) // 2
        self.xor_range(2 * node, lo, mid, l, r, z)
        self.xor_range(2 * node + 1, mid + 1, hi, l, r, z)
        self._pull(node)


def total_updates(arr, mat):
    n = len(arr)
    tree = SegTree(arr)
    total = 0
    for x, y, z in mat:
        start = x - 1
        mask = 1 << (y - 1)                       # y is 1-indexed: y = 1 is the least significant bit
        end = tree.first_zero_bit(1, 0, n - 1, start, mask)   # exclusive end of the run of set bits
        if end > start:
            total += end - start
            tree.xor_range(1, 0, n - 1, start, end - 1, z)
    return total

# ---- tests
import random
assert total_updates([2, 4, 3, 5, 4], [[3, 1, 4], [2, 3, 7]]) == 4
assert total_updates([1, 4], [[2, 1, 3]]) == 0
def brute(arr, mat):
    arr = list(arr); tot = 0
    for x, y, z in mat:
        i = x - 1
        while i < len(arr) and arr[i] >> (y - 1) & 1:
            arr[i] ^= z; tot += 1; i += 1
        # note: the run is determined before updating
    return tot
def brute2(arr, mat):
    arr = list(arr); tot = 0
    for x, y, z in mat:
        i = x - 1; j = i
        while j < len(arr) and arr[j] >> (y - 1) & 1: j += 1
        for t in range(i, j): arr[t] ^= z
        tot += j - i
    return tot
for _ in range(300):
    n = random.randint(1, 10)
    arr = [random.randint(0, 31) for _ in range(n)]
    mat = [[random.randint(1, n), random.randint(1, 5), random.randint(0, 31)] for _ in range(random.randint(1, 8))]
    assert total_updates(arr, mat) == brute2(arr, mat)
n = 100000
total_updates([random.randint(0, 10**9) for _ in range(n)], [[random.randint(1, n), random.randint(1, 30), random.randint(0, 10**9)] for _ in range(20000)])
print('ok')

def one_block(n, arr):
    ones = [i for i, v in enumerate(arr) if v == 1]
    if not ones:
        return 0
    ways = 1
    for i in range(1, len(ones)):
        ways *= ones[i] - ones[i - 1]         # the cut may be placed in this many gaps
    return ways

# ---- tests
import random
assert one_block(3, [0, 1, 0]) == 1
assert one_block(3, [0, 0, 0]) == 0
def brute(n, arr):
    cnt = 0
    for mask in range(1 << (n - 1)):          # bit i set = cut between i and i+1
        segs, start = [], 0
        for i in range(n - 1):
            if mask >> i & 1:
                segs.append(arr[start:i + 1]); start = i + 1
        segs.append(arr[start:])
        if all(sum(s) == 1 for s in segs):
            cnt += 1
    return cnt
for _ in range(300):
    n = random.randint(1, 10)
    arr = [random.randint(0, 1) for _ in range(n)]
    assert one_block(n, arr) == brute(n, arr)
print('ok')

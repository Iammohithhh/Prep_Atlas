from collections import deque


def min_jumps(nums):
    n = len(nums)
    dist = [-1] * n
    dist[0] = 0
    dq = deque([0])
    while dq:
        i = dq.popleft()
        if i == n - 1:
            return dist[i]
        for j in (i + 1, i + nums[i]):               # step to the next element, or jump nums[i] forward
            if j < n and dist[j] < 0:
                dist[j] = dist[i] + 1
                dq.append(j)
    return dist[n - 1]

# ---- tests
import random
assert min_jumps([2, 3, 1, 1, 4]) == 2
assert min_jumps([1]) == 0
assert min_jumps([0, 0, 0]) == 2
assert min_jumps([3, 0, 0, 0]) == 1
def brute(nums):
    n = len(nums); INF = 10**9; d = [INF] * n; d[0] = 0
    for i in range(n):
        for j in (i + 1, i + nums[i]):
            if j < n: d[j] = min(d[j], d[i] + 1)
    return d[n - 1]
for _ in range(300):
    a = [random.randint(0, 6) for _ in range(random.randint(1, 12))]
    assert min_jumps(a) == brute(a)
print('ok')

import random
from collections import deque
def orderPizza(orders, k):
    n = len(orders)
    res = []
    dq = deque()                     # indices of negative numbers in window
    for i in range(n):
        if orders[i] < 0: dq.append(i)
        if i >= k - 1:
            while dq and dq[0] <= i - k: dq.popleft()
            res.append(orders[dq[0]] if dq else 0)
    return res
def brute(orders, k):
    out = []
    for i in range(len(orders) - k + 1):
        w = orders[i:i+k]
        out.append(next((v for v in w if v < 0), 0))
    return out
assert orderPizza([-11, -2, 19, 37, 64, -18], 3) == [-11, -2, 0, -18]
for _ in range(300):
    n = random.randint(1, 10); k = random.randint(1, n)
    a = [random.randint(-5, 5) for _ in range(n)]
    a = [v if v != 0 else 1 for v in a]
    assert orderPizza(a, k) == brute(a, k)
print('ok')

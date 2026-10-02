import random
from bisect import bisect_left

def minPower(input1, input2, input3, input4):
    lamps = sorted(input4)
    ans = 0
    for b in input3:
        i = bisect_left(lamps, b)
        d = float('inf')
        if i < len(lamps): d = min(d, lamps[i] - b)
        if i > 0: d = min(d, b - lamps[i - 1])
        ans = max(ans, d)
    return ans

def brute(benches, lamps):
    for p in range(0, 200):
        if all(any(abs(b - l) <= p for l in lamps) for b in benches): return p

assert minPower(5, 3, [6,7,8,9,10], [6,10,8]) == 1
assert minPower(6, 4, [2,7,12,17,22,27], [5,10,15,20]) == 7
for _ in range(300):
    a = [random.randint(0, 30) for _ in range(random.randint(1, 6))]
    b = [random.randint(0, 30) for _ in range(random.randint(1, 4))]
    assert minPower(len(a), len(b), a, b) == brute(a, b)
print('ok')

import heapq


def get_server_index(n, arrival, burst):
    m = len(arrival)
    order = sorted(range(m), key=lambda i: (arrival[i], i))
    free = list(range(1, n + 1))                      # min-heap of free server ids
    heapq.heapify(free)
    busy = []                                         # min-heap of (finish time, server id)
    ans = [-1] * m
    for i in order:
        t = arrival[i]
        while busy and busy[0][0] <= t:
            _, sid = heapq.heappop(busy)
            heapq.heappush(free, sid)
        if free:
            sid = heapq.heappop(free)
            ans[i] = sid
            heapq.heappush(busy, (t + burst[i], sid))
    return ans

# ---- tests
import random
assert get_server_index(3, [2, 4, 1, 8, 9], [7, 9, 2, 4, 5]) == [2, 1, 1, 3, 2]
assert get_server_index(4, [3, 5, 1, 6, 8], [9, 2, 10, 4, 5]) == [2, 3, 1, 4, 3]
def brute(n, arr, b):
    m = len(arr); free_at = [0] * (n + 1); ans = [-1] * m
    for i in sorted(range(m), key=lambda i: (arr[i], i)):
        for s in range(1, n + 1):
            if free_at[s] <= arr[i]:
                ans[i] = s; free_at[s] = arr[i] + b[i]; break
    return ans
for _ in range(300):
    n = random.randint(1, 4); m = random.randint(1, 8)
    arr = [random.randint(1, 10) for _ in range(m)]; b = [random.randint(1, 6) for _ in range(m)]
    assert get_server_index(n, arr, b) == brute(n, arr, b)
print('ok')

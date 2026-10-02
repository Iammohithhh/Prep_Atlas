import heapq


def func(arr, n, k):
    res = [0] * (n + 1)
    res[1] = arr[0]
    for i in range(2, n + 1):
        res[i] = res[i - 1] + arr[i - 1]
    p = []                                     # min-heap holding the k largest subarray sums seen so far
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            res1 = res[j] - res[i - 1]
            if len(p) < k:
                heapq.heappush(p, res1)
            elif p[0] < res1:
                heapq.heapreplace(p, res1)
    return heapq.heappop(p)                    # the smallest of the k largest = the k-th largest

# ---- tests
arr = [2, -5, -7, 6, 4, 3, -10]
sums = sorted((sum(arr[i:j + 1]) for i in range(len(arr)) for j in range(i, len(arr))), reverse=True)
assert func(arr, 7, 3) == sums[2]
print(func(arr, 7, 3), sums[:5])
print('ok')

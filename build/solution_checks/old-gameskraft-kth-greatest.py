import heapq


def get_greatest_elements(arr, k):
    heap = []                                   # min-heap holding the k largest elements seen so far
    out = []
    for i, x in enumerate(arr):
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
        if i + 1 >= k:
            out.append(heap[0])                 # the smallest of the k largest = k-th greatest
    return out

# ---- tests
import random
assert get_greatest_elements([4, 2, 1, 3], 2) == [2, 2, 3]
assert get_greatest_elements([3, 2, 4, 5, 1], 4) == [2, 2]
assert get_greatest_elements([3, 1, 4, 5, 2], 2) == [1, 3, 4, 4]
for _ in range(300):
    n = random.randint(1, 10); a = list(range(1, n + 1)); random.shuffle(a); k = random.randint(1, n)
    assert get_greatest_elements(a, k) == [sorted(a[:i], reverse=True)[k - 1] for i in range(k, n + 1)]
print('ok')

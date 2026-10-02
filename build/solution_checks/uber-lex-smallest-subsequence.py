def smallest_subsequence(hubs, k):
    stack = []
    n = len(hubs)
    for i, h in enumerate(hubs):
        # pop larger tops while enough elements remain to still reach size k
        while stack and stack[-1] > h and len(stack) - 1 + (n - i) >= k:
            stack.pop()
        if len(stack) < k:
            stack.append(h)
    return stack

# ---- tests
import random
from itertools import combinations
assert smallest_subsequence([3, 1, 5, 3, 5, 9, 2], 4) == [1, 3, 5, 2]
for _ in range(300):
    n = random.randint(1, 8); a = [random.randint(1, 5) for _ in range(n)]
    k = random.randint(1, n)
    assert smallest_subsequence(a, k) == list(min(combinations(a, k))), (a, k)
print('ok')

def solution(n, heights):
    stack = []                                       # indices with increasing heights
    best = 0
    for i in range(n + 1):
        h = heights[i] if i < n else 0               # a sentinel bar of height 0 flushes the stack
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best

# ---- tests
import random
assert solution(8, [4, 1, 5, 3, 3, 2, 4, 1]) == 10
assert solution(1, [7]) == 7
for _ in range(300):
    n = random.randint(1, 10); h = [random.randint(1, 9) for _ in range(n)]
    exp = max(min(h[l:r + 1]) * (r - l + 1) for l in range(n) for r in range(l, n))
    assert solution(n, h) == exp
print('ok')

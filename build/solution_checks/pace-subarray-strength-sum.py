import random

MOD = 10**9 + 7

def getSubarrayStrengthSum(arr):
    n = len(arr)
    left = [0] * n            # number of choices for the left end (elements strictly smaller to the left)
    right = [0] * n           # number of choices for the right end (elements smaller or equal to the right)
    st = []
    for i in range(n):
        while st and arr[st[-1]] < arr[i]:
            st.pop()
        left[i] = i - (st[-1] if st else -1)
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and arr[st[-1]] <= arr[i]:
            st.pop()
        right[i] = (st[-1] if st else n) - i
        st.append(i)
    total = 0
    for i in range(n):
        lc, rc = left[i], right[i]
        total += arr[i] * (lc * rc * (lc + rc) // 2)
    return total % MOD

def brute(arr):
    n = len(arr)
    return sum((r - l + 1) * max(arr[l:r + 1]) for l in range(n) for r in range(l, n)) % MOD

assert getSubarrayStrengthSum([1, 2, 3]) == 25
assert getSubarrayStrengthSum([5, 9]) == 32
for _ in range(500):
    a = [random.randint(1, 6) for _ in range(random.randint(1, 10))]
    assert getSubarrayStrengthSum(a) == brute(a), a
print('ok')

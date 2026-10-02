MOD = 10**9 + 7


def find_number_of_partitions(arr):
    # B[t][u]: number of valid partitions of processed prefixes with prefix parity t whose last segment has parity u
    B = [[0, 0], [0, 0]]
    t = 0
    ans = 0
    for x in arr:
        t ^= x & 1
        # last segment parity = t xor (prefix parity at the previous cut); the previous segment must have the opposite parity
        ways_even = (B[t][1] + (1 if t == 0 else 0)) % MOD
        ways_odd = (B[t ^ 1][0] + (1 if t == 1 else 0)) % MOD
        B[t][0] = (B[t][0] + ways_even) % MOD
        B[t][1] = (B[t][1] + ways_odd) % MOD
        ans = (ways_even + ways_odd) % MOD
    return ans

# ---- tests
import random
assert find_number_of_partitions([1, 2, 3, 3]) == 4
assert find_number_of_partitions([1, 1, 1, 1]) == 2
def brute(arr):
    n = len(arr); cnt = 0
    for mask in range(1 << (n - 1)):
        segs = []; cur = arr[0]
        for i in range(1, n):
            if mask >> (i - 1) & 1: segs.append(cur); cur = arr[i]
            else: cur += arr[i]
        segs.append(cur)
        if all((segs[i] - segs[i + 1]) % 2 for i in range(len(segs) - 1)): cnt += 1
    return cnt % MOD
for _ in range(500):
    a = [random.randint(1, 9) for _ in range(random.randint(1, 10))]
    assert find_number_of_partitions(a) == brute(a), a
print('ok')

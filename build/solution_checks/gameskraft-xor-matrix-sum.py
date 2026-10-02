MOD = 10**9 + 7


def get_maximum_xor_sum(arr1, arr2):
    n = len(arr1)
    total = 0
    for bit in range(31):                            # values are below 2^30
        ones1 = sum((x >> bit) & 1 for x in arr1)
        ones2 = sum((x >> bit) & 1 for x in arr2)
        # XOR bit is 1 when exactly one of the two bits is 1
        pairs = ones1 * (n - ones2) + (n - ones1) * ones2
        total = (total + pairs * (1 << bit)) % MOD
    return total

# ---- tests
import random
assert get_maximum_xor_sum([1, 2, 3, 4], [1, 2, 3, 4]) == 48
assert get_maximum_xor_sum([1, 2, 3], [10, 10, 10]) == 84
for _ in range(300):
    n = random.randint(1, 8)
    a = [random.randint(1, 10**9) for _ in range(n)]; b = [random.randint(1, 10**9) for _ in range(n)]
    assert get_maximum_xor_sum(a, b) == sum(x ^ y for x in a for y in b) % MOD
print('ok')

def get_max_value_sum(encrypted_file, binary, k):
    n = len(encrypted_file)
    base = sum(v for v, b in zip(encrypted_file, binary) if b == 1)
    gain = [v if b == 0 else 0 for v, b in zip(encrypted_file, binary)]   # value gained if this file gets decrypted
    window = sum(gain[:k])
    best = window
    for i in range(k, n):
        window += gain[i] - gain[i - k]
        best = max(best, window)
    return base + best

# ---- tests
import random
assert get_max_value_sum([1, 3, 5, 2, 5, 4], [1, 1, 0, 1, 0, 0], 3) == 16
def brute(v, b, k):
    n = len(v); best = 0
    for i in range(n - k + 1):
        t = sum(v[j] for j in range(n) if b[j] == 1 or i <= j < i + k)
        best = max(best, t)
    return best
for _ in range(300):
    n = random.randint(1, 9); k = random.randint(1, n)
    v = [random.randint(1, 9) for _ in range(n)]; b = [random.randint(0, 1) for _ in range(n)]
    assert get_max_value_sum(v, b, k) == brute(v, b, k)
print('ok')

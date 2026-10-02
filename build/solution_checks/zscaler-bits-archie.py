def count_bit(arr, k):
    cnt = [0] * 40
    for x in arr:
        cnt[bin(x).count('1')] += 1
    total = 0
    for a in range(40):
        for b in range(a, 40):
            if a + b >= k:
                total += cnt[a] * (cnt[a] - 1) // 2 if a == b else cnt[a] * cnt[b]
    return total

# ---- tests
import random
assert count_bit([2, 4, 6, 8, 10], 4) == 1
assert count_bit([3, 1, 9, 8], 3) == 5
for _ in range(300):
    a = [random.randint(1, 200) for _ in range(random.randint(1, 12))]; k = random.randint(1, 12)
    exp = sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if bin(a[i] | a[j]).count('1') + bin(a[i] & a[j]).count('1') >= k)
    assert count_bit(a, k) == exp
print('ok')

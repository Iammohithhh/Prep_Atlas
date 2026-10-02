def bin_addition(a, b):
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    out = []
    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += int(a[i]); i -= 1
        if j >= 0:
            total += int(b[j]); j -= 1
        out.append(str(total & 1))
        carry = total >> 1
    res = ''.join(reversed(out)).lstrip('0')
    return res or '0'

# ---- tests
import random
assert bin_addition("100", "010") == "110"
assert bin_addition("111", "11") == "1010"
assert bin_addition("0", "0") == "0"
for _ in range(300):
    x, y = random.randint(0, 2000), random.randint(0, 2000)
    assert bin_addition(bin(x)[2:], bin(y)[2:]) == bin(x + y)[2:]
print('ok')

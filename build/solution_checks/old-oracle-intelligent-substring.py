def get_special_substring(s, k, char_value):
    normal = [c == '0' for c in char_value]
    left = 0
    count = 0
    best = 0
    for right, ch in enumerate(s):
        if normal[ord(ch) - 97]:
            count += 1
        while count > k:
            if normal[ord(s[left]) - 97]:
                count -= 1
            left += 1
        best = max(best, right - left + 1)
    return best

# ---- tests
import random
assert get_special_substring("giraffe", 2, "01111001111111111011111111") == 3
assert get_special_substring("abcde", 2, "10101111111111111111111111") == 5
for _ in range(300):
    cv = ''.join(random.choice('01') for _ in range(26)); s = ''.join(random.choice('abcde') for _ in range(random.randint(1, 10))); k = random.randint(0, 4)
    exp = max((j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if sum(cv[ord(c) - 97] == '0' for c in s[i:j]) <= k), default=0)
    assert get_special_substring(s, k, cv) == exp
print('ok')

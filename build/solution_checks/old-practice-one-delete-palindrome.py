def valid_palindrome(s):
    def is_pal(i, j):
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return is_pal(i + 1, j) or is_pal(i, j - 1)   # delete the left or the right character
        i += 1
        j -= 1
    return True

# ---- tests
import random
assert valid_palindrome("")
assert valid_palindrome("abca")
assert not valid_palindrome("abc")
assert valid_palindrome("a")
def brute(s):
    if s == s[::-1]:
        return True
    return any((s[:i] + s[i + 1:]) == (s[:i] + s[i + 1:])[::-1] for i in range(len(s)))
for _ in range(500):
    s = ''.join(random.choice('abc') for _ in range(random.randint(0, 9)))
    assert valid_palindrome(s) == brute(s), s
print('ok')

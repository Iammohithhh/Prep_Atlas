def longest_valid_parentheses(s):
    stack = [-1]                              # index just before the current valid run
    best = 0
    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)               # unmatched ')': new base
            else:
                best = max(best, i - stack[-1])
    return best

# ---- tests
import random
assert longest_valid_parentheses("(()") == 2
assert longest_valid_parentheses(")()())") == 4
assert longest_valid_parentheses("") == 0
def brute(s):
    best = 0
    for i in range(len(s)):
        bal = 0
        for j in range(i, len(s)):
            bal += 1 if s[j] == '(' else -1
            if bal < 0:
                break
            if bal == 0:
                best = max(best, j - i + 1)
    return best
for _ in range(500):
    s = ''.join(random.choice('()') for _ in range(random.randint(0, 12)))
    assert longest_valid_parentheses(s) == brute(s), s
print('ok')

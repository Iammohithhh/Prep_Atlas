import re

PATTERN = re.compile(r'^[a-z]{1,6}_?[0-9]{0,4}@hackerrank\.com$')


def check(queries):
    return [bool(PATTERN.match(q)) for q in queries]

# ---- tests
assert check(["julia@hackerrank.com", "julia_@hackerrank.com", "julia_0@hackerrank.com", "julia0_@hackerrank.com", "julia@gmail.com"]) == [True, True, True, False, False]
assert check(["abcdef1234@hackerrank.com"]) == [True]       # digits without underscore are allowed
assert check(["a7_1@baddomain.com"]) == [False]
assert check(["abcdefg@hackerrank.com"]) == [False]          # 7 letters
print('ok')

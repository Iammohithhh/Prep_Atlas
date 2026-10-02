def number_of_subint(m, k):
    s = str(m)
    count = 0
    for i in range(len(s) - k + 1):
        v = int(s[i:i + k])
        if v != 0 and m % v == 0:
            count += 1
    return count

# ---- tests
assert number_of_subint(500, 1) == 1
assert number_of_subint(224, 2) == 0
assert number_of_subint(1224, 1) == 4
assert number_of_subint(12, 1) == 2
print('ok')

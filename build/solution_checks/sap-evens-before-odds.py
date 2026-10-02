import random
def arrange(a):
    return [v for v in a if v % 2 == 0] + [v for v in a if v % 2 != 0]
assert arrange([10, 98, 3, 33, 12, 22, 21, 11]) == [10, 98, 12, 22, 3, 33, 21, 11]
assert arrange([-3, 2, -4]) == [2, -4, -3]   # Python % keeps negatives correct
for _ in range(200):
    a = [random.randint(-9, 9) for _ in range(random.randint(0, 8))]
    r = arrange(a)
    assert sorted(r) == sorted(a)
print('ok')

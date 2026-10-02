import random
from collections import defaultdict

def smallest(a):
    groups = defaultdict(list); pos = defaultdict(list)
    for i, v in enumerate(a):
        groups[v >> 2].append(v); pos[v >> 2].append(i)
    res = a[:]
    for g in groups:
        for i, v in zip(pos[g], sorted(groups[g])): res[i] = v
    return res

def brute(a):
    seen = {tuple(a)}; st = [tuple(a)]
    while st:
        cur = st.pop()
        for i in range(len(cur)):
            for j in range(i + 1, len(cur)):
                if cur[i] ^ cur[j] < 4:
                    nx = list(cur); nx[i], nx[j] = nx[j], nx[i]; nx = tuple(nx)
                    if nx not in seen: seen.add(nx); st.append(nx)
    return list(min(seen))

assert smallest([1, 0, 3, 2]) == [0, 1, 2, 3]
assert smallest([2, 7, 1, 5, 6]) == [1, 5, 2, 6, 7]
for _ in range(300):
    n = random.randint(1, 6)
    a = [random.randint(0, 12) for _ in range(n)]
    assert smallest(a) == brute(a), a
print('ok')

import random
from collections import defaultdict

def smallest(s, arr):
    pos = defaultdict(list)
    for i, w in enumerate(arr):
        pos[w].append(i)
    res = list(s)
    for w, idx in pos.items():
        for i, ch in zip(idx, sorted(s[i] for i in idx)):
            res[i] = ch
    return ''.join(res)

def brute(s, arr):
    n = len(s)
    seen = {s}
    st = [s]
    while st:
        cur = st.pop()
        for i in range(n):
            for j in range(i + 1, n):
                if arr[i] == arr[j]:
                    t = list(cur)
                    t[i], t[j] = t[j], t[i]
                    t = ''.join(t)
                    if t not in seen:
                        seen.add(t)
                        st.append(t)
    return min(seen)

assert smallest('xvrb', [2, 1, 2, 2]) == 'bvrx'
for _ in range(300):
    n = random.randint(1, 6)
    s = ''.join(random.choice('abcd') for _ in range(n))
    arr = [random.randint(1, 3) for _ in range(n)]
    assert smallest(s, arr) == brute(s, arr)
print('ok')

import random

def count(arr):
    present = set(arr)
    ans = 0
    cur = {}                                   # OR value -> number of subarray starts
    for x in arr:
        nxt = {x: 1}
        for v, c in cur.items():
            nxt[v | x] = nxt.get(v | x, 0) + c
        cur = nxt
        ans += sum(c for v, c in cur.items() if v in present)
    return ans

def brute(a):
    s = set(a)
    c = 0
    for i in range(len(a)):
        o = 0
        for j in range(i, len(a)):
            o |= a[j]
            if o in s:
                c += 1
    return c

assert count([2, 4, 7]) == 5
for _ in range(500):
    a = [random.randint(0, 15) for _ in range(random.randint(1, 10))]
    assert count(a) == brute(a)
print('ok')

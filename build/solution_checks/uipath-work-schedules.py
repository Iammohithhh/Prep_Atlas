import random
from itertools import product

def findSchedules(workHours, dayHours, pattern):
    fixed = sum(int(c) for c in pattern if c != '?')
    need = workHours - fixed
    out = []
    def rec(i, rem, cur):
        if i == len(pattern):
            if rem == 0:
                out.append(''.join(cur))
            return
        if pattern[i] != '?':
            cur.append(pattern[i])
            rec(i + 1, rem, cur)
            cur.pop()
        else:
            left = pattern[i + 1:].count('?')
            for d in range(0, min(dayHours, rem) + 1):
                if rem - d <= left * dayHours:
                    cur.append(str(d))
                    rec(i + 1, rem - d, cur)
                    cur.pop()
    if need >= 0:
        rec(0, need, [])
    return out

def brute(w, d, p):
    qs = [i for i, c in enumerate(p) if c == '?']
    res = []
    for digs in product(range(d + 1), repeat=len(qs)):
        s = list(p)
        for i, v in zip(qs, digs):
            s[i] = str(v)
        if sum(int(c) for c in s) == w:
            res.append(''.join(s))
    return sorted(res)

assert findSchedules(24, 4, '08??840') == ['0804840', '0813840', '0822840', '0831840', '0840840']
for _ in range(200):
    p = ''.join(random.choice('0123?') for _ in range(7))
    w = random.randint(0, 25)
    d = random.randint(1, 8)
    assert findSchedules(w, d, p) == brute(w, d, p)
print('ok')

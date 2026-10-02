import random
from collections import defaultdict, OrderedDict

def implementLFU(cacheSize, queries):
    vals = {}
    freq = {}
    buckets = defaultdict(OrderedDict)          # frequency -> keys, oldest use first
    minf = 0
    out = []

    def touch(k):
        nonlocal minf
        f = freq[k]
        del buckets[f][k]
        if not buckets[f] and minf == f:
            minf += 1
        freq[k] = f + 1
        buckets[f + 1][k] = None

    for q in queries:
        p = q.split()
        if p[0] == 'GET':
            k = p[1]
            if k in vals:
                touch(k)
                out.append(int(vals[k]))
            else:
                out.append(-1)
        else:
            k, v = p[1], p[2]
            if cacheSize == 0:
                continue
            if k in vals:
                vals[k] = v
                touch(k)
            else:
                if len(vals) >= cacheSize:
                    old, _ = buckets[minf].popitem(last=False)
                    del vals[old]
                    del freq[old]
                vals[k] = v
                freq[k] = 1
                buckets[1][k] = None
                minf = 1
    return out

def brute(cap, queries):
    d = {}
    t = 0
    out = []
    for q in queries:
        p = q.split()
        t += 1
        if p[0] == 'GET':
            k = p[1]
            if k in d:
                v, f, _ = d[k]
                d[k] = (v, f + 1, t)
                out.append(int(v))
            else:
                out.append(-1)
        else:
            k, v = p[1], p[2]
            if k in d:
                d[k] = (v, d[k][1] + 1, t)
            else:
                if len(d) >= cap:
                    victim = min(d, key=lambda x: (d[x][1], d[x][2]))
                    del d[victim]
                d[k] = (v, 1, t)
    return out

assert implementLFU(2, ["PUT 1 1", "PUT 2 2", "PUT 3 3", "GET 1"]) == [-1]
assert implementLFU(2, ["PUT 1 1", "PUT 2 2", "GET 1", "PUT 3 3", "GET 2"]) == [1, -1]
for _ in range(500):
    cap = random.randint(1, 3)
    qs = []
    for _ in range(random.randint(1, 15)):
        k = random.randint(1, 4)
        qs.append(f"GET {k}" if random.random() < 0.4 else f"PUT {k} {random.randint(1, 9)}")
    assert implementLFU(cap, qs) == brute(cap, qs), (cap, qs)
print('ok')

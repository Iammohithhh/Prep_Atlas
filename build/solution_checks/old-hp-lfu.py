from collections import defaultdict, OrderedDict


def implement_lfu(cache_size, queries):
    val, freq = {}, {}
    buckets = defaultdict(OrderedDict)         # frequency -> keys in least-recent-first order
    min_freq = 0
    out = []

    def touch(k):
        nonlocal min_freq
        f = freq[k]
        del buckets[f][k]
        if not buckets[f]:
            del buckets[f]
            if min_freq == f:
                min_freq += 1
        freq[k] = f + 1
        buckets[f + 1][k] = None

    for q in queries:
        parts = q.split()
        if parts[0] == 'GET':
            k = int(parts[1])
            if k in val:
                touch(k)
                out.append(val[k])
            else:
                out.append(-1)
        else:
            k, v = int(parts[1]), int(parts[2])
            if cache_size <= 0:
                continue
            if k in val:
                val[k] = v
                touch(k)                       # an update counts as a use
            else:
                if len(val) >= cache_size:
                    old, _ = buckets[min_freq].popitem(last=False)
                    if not buckets[min_freq]:
                        del buckets[min_freq]
                    del val[old]; del freq[old]
                val[k] = v; freq[k] = 1
                buckets[1][k] = None
                min_freq = 1
    return out

# ---- tests
import random
assert implement_lfu(2, ["PUT 1 1", "PUT 2 2", "GET 1", "PUT 3 3", "GET 2"]) == [1, -1]
def brute(cap, queries):
    store = {}                                  # key -> [value, uses, last_time]
    t = 0; out = []
    for q in queries:
        t += 1
        p = q.split()
        if p[0] == 'GET':
            k = int(p[1])
            if k in store:
                store[k][1] += 1; store[k][2] = t; out.append(store[k][0])
            else:
                out.append(-1)
        else:
            k, v = int(p[1]), int(p[2])
            if cap <= 0:
                continue
            if k in store:
                store[k][0] = v; store[k][1] += 1; store[k][2] = t
            else:
                if len(store) >= cap:
                    victim = min(store, key=lambda x: (store[x][1], store[x][2]))
                    del store[victim]
                store[k] = [v, 1, t]
    return out
for _ in range(500):
    cap = random.randint(1, 3)
    qs = []
    for _ in range(random.randint(1, 14)):
        if random.random() < 0.5:
            qs.append(f"PUT {random.randint(1, 4)} {random.randint(1, 9)}")
        else:
            qs.append(f"GET {random.randint(1, 4)}")
    assert implement_lfu(cap, qs) == brute(cap, qs), (cap, qs)
print('ok')

import heapq


def get_unexpired_tokens(time_to_live, queries):
    expiry = {}                                    # token -> current expiry time
    heap = []                                      # (expiry, token) entries, possibly stale
    out = []

    def purge(now):
        while heap and heap[0][0] <= now:          # expiry at `now` counts as expired
            e, tok = heapq.heappop(heap)
            if expiry.get(tok) == e:
                del expiry[tok]

    for q in queries:
        parts = q.split()
        kind = parts[0]
        if kind == 'generate':
            tok, t = parts[1], int(parts[2])
            purge(t)
            expiry[tok] = t + time_to_live
            heapq.heappush(heap, (t + time_to_live, tok))
        elif kind == 'renew':
            tok, t = parts[1], int(parts[2])
            purge(t)
            if tok in expiry:
                expiry[tok] = t + time_to_live
                heapq.heappush(heap, (t + time_to_live, tok))
        else:
            t = int(parts[1])
            purge(t)
            out.append(len(expiry))
    return out

# ---- tests
import random
assert get_unexpired_tokens(5, ["generate aaa 1", "renew aaa 2", "count 6", "generate bbb 7", "renew aaa 8", "renew bbb 10", "count 15"]) == [1, 0]
assert get_unexpired_tokens(35, ["generate token1 3", "count 4", "generate token2 6", "count 7", "generate token3 11", "count 41"]) == [1, 2, 1]
def brute(ttl, qs):
    exp = {}; out = []
    for q in qs:
        p = q.split(); t = int(p[-1])
        exp = {k: v for k, v in exp.items() if v > t}
        if p[0] == 'generate': exp[p[1]] = t + ttl
        elif p[0] == 'renew':
            if p[1] in exp: exp[p[1]] = t + ttl
        else: out.append(len(exp))
    return out
for _ in range(300):
    ttl = random.randint(1, 6); t = 0; qs = []; used = 0
    for _ in range(random.randint(1, 12)):
        t += random.randint(0, 3); r = random.random()
        if r < .35: qs.append(f'generate t{used} {t}'); used += 1
        elif r < .65 and used: qs.append(f'renew t{random.randint(0, used - 1)} {t}')
        else: qs.append(f'count {t}')
    assert get_unexpired_tokens(ttl, qs) == brute(ttl, qs), (ttl, qs)
print('ok')

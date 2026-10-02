import random

def longestChain(words):
    best = {}
    for w in sorted(set(words), key=len):
        b = 1
        for i in range(len(w)):
            p = w[:i] + w[i + 1:]
            if p in best:
                b = max(b, best[p] + 1)
        best[w] = b
    return max(best.values())

def brute(words):
    S = set(words)
    def f(w):
        r = 1
        for i in range(len(w)):
            p = w[:i] + w[i + 1:]
            if p in S:
                r = max(r, 1 + f(p))
        return r
    return max(f(w) for w in S)

assert longestChain(['a', 'b', 'ba', 'bca', 'bda', 'bdca']) == 4
assert longestChain(['a', 'and', 'an', 'bear']) == 3
for _ in range(300):
    ws = [''.join(random.choice('abc') for _ in range(random.randint(1, 5))) for _ in range(random.randint(1, 10))]
    assert longestChain(ws) == brute(ws)
print('ok')

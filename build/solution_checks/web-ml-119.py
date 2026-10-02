def evaluate(queries, relevant, api, k, retries=2):
    precs, recs, failures = [], [], 0
    for q in queries:
        res = None
        for _ in range(retries + 1):
            try:
                res = api(q, k)
                break
            except Exception:
                continue
        if res is None:
            failures += 1
            res = []
        seen, items = set(), []
        for r in res:
            if r not in seen:
                seen.add(r)
                items.append(r)
        items = items[:k]
        rel = relevant[q]
        hits = sum(1 for r in items if r in rel)
        precs.append(hits / k)
        recs.append(hits / len(rel) if rel else 0.0)
    n = len(queries)
    return sum(precs) / n, sum(recs) / n, failures / n

calls = {'n': 0}
def api(q, k):
    calls['n'] += 1
    if q == 'bad':
        raise RuntimeError('down')
    return {'a': ['x', 'x', 'y', 'z'], 'b': ['p']}[q]
rel = {'a': {'x', 'z', 'w'}, 'b': {'p'}, 'bad': {'u'}}
p, r, f = evaluate(['a', 'b', 'bad'], rel, api, k=3)
# a: items x,y,z -> hits 2 -> p 2/3, r 2/3 ; b: hits 1 -> p 1/3, r 1 ; bad: 0, 0
assert abs(p - (2 / 3 + 1 / 3 + 0) / 3) < 1e-12 and abs(r - (2 / 3 + 1 + 0) / 3) < 1e-12 and abs(f - 1 / 3) < 1e-12
assert calls['n'] == 1 + 1 + 3                           # the failing query was retried twice
print("ok")

from collections import defaultdict

def rolling_mean_by_group(rows, window=3):
    by = defaultdict(list)
    for ent, ts, val in rows:
        by[ent].append((ts, val))
    out = {}
    for ent, items in by.items():
        items.sort()
        vals = [v for _, v in items]
        run, res = 0.0, []
        for i, v in enumerate(vals):
            run += v
            if i >= window:
                run -= vals[i - window]
            res.append(run / min(i + 1, window) if i + 1 >= window else None)
        out[ent] = [(ts, m) for (ts, _), m in zip(items, res)]
    return out

rows = [('a', 3, 30), ('a', 1, 10), ('a', 2, 20), ('b', 1, 5), ('b', 2, 7), ('a', 4, 40)]
res = rolling_mean_by_group(rows, window=3)
assert res['a'] == [(1, None), (2, None), (3, 20.0), (4, 30.0)]
assert res['b'] == [(1, None), (2, None)]
print("ok")

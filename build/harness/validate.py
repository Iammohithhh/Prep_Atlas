"""Build verified test cases for one question.

Usage: python validate.py JOB_JSON OUT_JSON
JOB: {"code", "function", "params", "examples": [{"input","output"}], "captures": [{"function": name, "path": file}]}
The published solution code is executed; a case is kept only if the solution reproduces
its expected value exactly (twice, to drop nondeterministic results).
"""
import ast
import json
import math
import sys

job = json.load(open(sys.argv[1], encoding='utf-8'))
OUT = sys.argv[2]
MAX_CASE_CHARS = 3000
SAFE = 2 ** 53


def dec(v):
    if isinstance(v, dict) and '__nd__' in v:
        import numpy as np
        return np.array(dec(v['__nd__']), dtype=v.get('dtype'))
    if isinstance(v, list):
        return [dec(x) for x in v]
    if isinstance(v, dict):
        return {k: dec(x) for k, x in v.items()}
    return v


def enc(v):
    if v is None or isinstance(v, (bool, str)):
        return v
    if isinstance(v, int):
        if abs(v) > SAFE:
            raise ValueError('unsafe int')
        return v
    if isinstance(v, float):
        if not math.isfinite(v):
            raise ValueError('non-finite')
        return v
    if isinstance(v, (list, tuple)):
        return [enc(x) for x in v]
    if isinstance(v, dict) and all(isinstance(k, str) for k in v):
        return {k: enc(x) for k, x in v.items()}
    if type(v).__module__ == 'numpy':
        import numpy as np
        if isinstance(v, np.ndarray):
            return {'__nd__': enc(v.tolist()), 'dtype': str(v.dtype)}
        return enc(v.item())
    raise ValueError('unencodable ' + type(v).__name__)


def norm(v):
    if type(v).__module__ == 'numpy':
        v = v.tolist()
    if isinstance(v, tuple):
        v = list(v)
    if isinstance(v, list):
        return [norm(x) for x in v]
    if isinstance(v, dict):
        return {k: norm(x) for k, x in v.items()}
    return v


def equal(a, b):
    a, b = norm(a), norm(b)
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-8)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(equal(a[k], b[k]) for k in a)
    return a == b


def split_top(text):
    """Split on commas / newlines / semicolons that are not inside brackets or quotes."""
    parts, depth, cur, quote = [], 0, '', None
    for ch in text:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
            continue
        if ch in '"\'':
            quote = ch
        elif ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth -= 1
        if ch in ',;\n' and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def lit(s):
    s = s.strip().rstrip('.')
    low = s.lower()
    if low in ('true', 'false'):
        return low == 'true'
    if low in ('null', 'none'):
        return None
    try:
        return ast.literal_eval(s)
    except Exception:
        pass
    try:
        return ast.literal_eval(s.replace('true', 'True').replace('false', 'False'))
    except Exception:
        raise ValueError('not a literal: ' + s[:60])


def parse_args(text, params):
    text = text.replace('−', '-').replace('“', '"').replace('”', '"').replace("’", "'")
    pieces = split_top(text)
    named = []
    for p in pieces:
        if '=' in p and '==' not in p.split('=', 1)[0]:
            k, v = p.split('=', 1)
            named.append((k.strip().strip('`'), v.strip()))
        else:
            named.append((None, p))
    if all(k for k, _ in named):
        values = {k: lit(v) for k, v in named}
        if set(values) == set(params):
            return [values[p] for p in params]
        if len(values) == len(params):
            return list(values.values())
    if len(pieces) == len(params):
        return [lit(p.split('=', 1)[-1] if '=' in p else p) for p in pieces]
    if len(params) == 1:
        return [lit(text)]
    raise ValueError('cannot map example to parameters')


ns = {'__name__': 'harness'}
exec(compile(job['code'], '<solution>', 'exec'), ns)
fn = ns[job['function']]
params = job['params']


def run(args):
    import copy
    return fn(*copy.deepcopy(dec(args)))


def verified(args, expected):
    """True when the published solution returns `expected` for `args`, deterministically."""
    try:
        got1, got2 = run(args), run(args)
    except Exception:
        return False
    return equal(got1, expected) and equal(got2, expected)


report = {'examples_total': len(job['examples']), 'examples_ok': 0, 'notes': []}
samples, seen = [], set()
for ex in job['examples']:
    try:
        args = enc(parse_args(ex['input'], params))
        expected = lit(ex['output'])
        if verified(args, expected):
            key = json.dumps(args, sort_keys=True)
            if key not in seen:
                seen.add(key)
                samples.append({'args': args, 'expected': enc(norm(run(args)))})
                report['examples_ok'] += 1
        else:
            report['notes'].append('example disagrees with solution or failed to run')
    except Exception as e:
        report['notes'].append('example not parsed: ' + str(e)[:80])

hidden = []
for cap in job['captures']:
    try:
        recs = json.load(open(cap['path'], encoding='utf-8')).get(cap['function'], [])
    except Exception:
        continue
    for r in recs:
        if len(r['args']) != len(params):
            continue
        key = json.dumps(r['args'], sort_keys=True)
        if key in seen or len(key) > MAX_CASE_CHARS:
            continue
        try:
            if verified(r['args'], dec(r['ret'])):
                seen.add(key)
                hidden.append({'args': r['args'], 'expected': enc(norm(run(r['args'])))})
        except Exception:
            continue

# Spread hidden cases over sizes: smallest first, then a stride through the rest; at most 20.
hidden.sort(key=lambda c: len(json.dumps(c['args'])))
if len(hidden) > 20:
    step = len(hidden) / 20
    hidden = [hidden[int(i * step)] for i in range(20)]
if not samples and hidden:
    samples, hidden = hidden[:2], hidden[2:]
report['hidden'] = len(hidden)
numpy_io = any('__nd__' in json.dumps(c) for c in samples + hidden)
out = {'cases': samples + hidden, 'samples': len(samples), 'numpy': numpy_io, 'report': report}
json.dump(out, open(OUT, 'w', encoding='utf-8'))

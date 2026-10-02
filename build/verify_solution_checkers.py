"""Every question with test cases: its published solution code must pass ALL of them.

Uses the same comparison as site/python-worker.js (tuples == lists, numpy -> lists, float tolerance)
and the same block choice as "Load into editor". Usage: python build/verify_solution_checkers.py
"""
import copy
import json
import math
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def dec(v):
    if isinstance(v, dict) and '__nd__' in v:
        import numpy as np
        return np.array(dec(v['__nd__']), dtype=v.get('dtype'))
    if isinstance(v, list):
        return [dec(x) for x in v]
    if isinstance(v, dict):
        return {k: dec(x) for k, x in v.items()}
    return v


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


def check(q):
    ch = q['checker']
    blocks = re.findall(r'```(?:python|py)\n([\s\S]*?)```', q.get('solution', ''))
    code = next((b for b in blocks if re.search(rf'^def {ch["function"]}\s*\(', b, re.M)), blocks[0] if blocks else None)
    if not code:
        return q['id'], 'NO CODE'
    ns = {'__name__': 'verify'}
    try:
        exec(code, ns)
    except Exception as e:
        return q['id'], f'EXEC FAIL {e!r}'[:120]
    fn = ns.get(ch['function'])
    if not callable(fn):
        return q['id'], f'NAME: needs {ch["function"]}'
    fails = 0
    for case in ch['cases']:
        try:
            ok = equal(fn(*copy.deepcopy(dec(case['args']))), dec(case['expected']))
        except Exception:
            ok = False
        fails += not ok
    return q['id'], 'OK' if not fails else f'{fails}/{len(ch["cases"])} FAIL'


if __name__ == '__main__':
    qs = [q for q in json.loads((ROOT / 'site/data/questions.json').read_text(encoding='utf-8'))['questions'] if q.get('checker')]
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(check, qs, timeout=600))
    bad = [(i, s) for i, s in results if s != 'OK']
    for i, s in bad:
        print(f'{s:24s} {i}')
    print(f'questions with tests: {len(results)} | passing: {len(results) - len(bad)} | problems: {len(bad)}')
    sys.exit(1 if bad else 0)

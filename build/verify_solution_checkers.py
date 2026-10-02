"""For every question with practice checks, run the Python code from its written solution against those checks.

Loading a solution into the editor must pass "Check solution". Usage: python build/verify_solution_checkers.py
"""
import json
import math
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
qs = json.loads((ROOT / 'site/data/questions.json').read_text(encoding='utf-8'))['questions']


def close(a, b, tol):
    if isinstance(a, np.ndarray):
        a = a.tolist()
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if tol and isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=tol, abs_tol=tol)
    return a == b


bad = 0
for q in (q for q in qs if q.get('checker')):
    ch = q['checker']
    blocks = re.findall(r'```(?:python|py)\n([\s\S]*?)```', q.get('solution', ''))
    # Same choice as the site's "Load into editor": the block defining the checked function, else the first.
    code = next((b for b in blocks if re.search(rf'^def {ch["function"]}\s*\(', b, re.M)), blocks[0] if blocks else None)
    if not code:
        print(f'NO CODE   {q["id"]}'); bad += 1; continue
    ns = {}
    try:
        exec(code, ns)
    except Exception as e:
        print(f'EXEC FAIL {q["id"]}: {e!r}'); bad += 1; continue
    fn = ns.get(ch['function'])
    if not callable(fn):
        defs = re.findall(r'^def (\w+)', code, re.M)
        print(f'NAME      {q["id"]}: needs {ch["function"]}, solution defines {defs}'); bad += 1; continue
    tol = 1e-6 if ch.get('float') or ch.get('numpy') else 0
    fails = 0
    for case in ch['cases']:
        args = [np.array(a) if ch.get('numpy') and isinstance(a, list) else a for a in case['args']]
        try:
            ok = close(fn(*args), case['expected'], tol)
        except Exception:
            ok = False
        fails += not ok
    status = 'OK' if not fails else f'{fails}/{len(ch["cases"])} FAIL'
    bad += bool(fails)
    print(f'{status:9s} {q["id"]}')
print('problems:', bad)

"""Run one solution-check script and record outermost calls to its top-level functions.

Usage: python capture.py SCRIPT OUT_JSON
Writes {function_name: [{"args": [...], "ret": ...}, ...]} with JSON-safe encodings
(tuples -> lists, numpy arrays -> {"__nd__": list, "dtype": str}). Values that can't be
encoded, or integers beyond 2**53 (unsafe in the browser), are dropped.
"""
import copy
import json
import runpy
import sys

SCRIPT, OUT = sys.argv[1], sys.argv[2]
LIMIT = 250
SAFE = 2 ** 53


class Skip(Exception):
    pass


def enc(v, depth=0):
    if depth > 40:
        raise Skip
    if v is None or isinstance(v, (bool, str)):
        return v
    if isinstance(v, int):
        if abs(v) > SAFE:
            raise Skip
        return v
    if isinstance(v, float):
        if v != v or v in (float('inf'), float('-inf')):
            raise Skip
        return v
    if isinstance(v, (list, tuple)):
        return [enc(x, depth + 1) for x in v]
    if isinstance(v, dict):
        if not all(isinstance(k, str) for k in v):
            raise Skip
        return {k: enc(x, depth + 1) for k, x in v.items()}
    mod = type(v).__module__
    if mod == 'numpy':
        import numpy as np
        if isinstance(v, np.ndarray):
            return {'__nd__': enc(v.tolist(), depth + 1), 'dtype': str(v.dtype)}
        if isinstance(v, np.generic):
            return enc(v.item(), depth + 1)
    raise Skip


records = {}
active = {}  # id(frame) -> (name, encoded args)


def prof(frame, event, arg):
    code = frame.f_code
    if code.co_filename != SCRIPT or '.' in code.co_qualname or code.co_name.startswith('<'):
        return
    name = code.co_name
    if event == 'call':
        back = frame.f_back
        if back is not None and back.f_code.co_name == name and back.f_code.co_filename == SCRIPT:
            return  # recursive inner call: only the outermost call is a test case
        if len(records.get(name, [])) >= LIMIT:
            return
        try:
            params = code.co_varnames[:code.co_argcount]
            args = [enc(copy.deepcopy(frame.f_locals[p])) for p in params]
        except Exception:
            return
        active[id(frame)] = (name, args)
    elif event == 'return' and id(frame) in active:
        name, args = active.pop(id(frame))
        try:
            records.setdefault(name, []).append({'args': args, 'ret': enc(arg)})
        except Exception:
            pass


sys.setprofile(prof)
try:
    runpy.run_path(SCRIPT, run_name='__main__')
except SystemExit:
    pass
except BaseException as e:  # a failing check script still yields whatever it recorded
    records['__error__'] = repr(e)[:300]
finally:
    sys.setprofile(None)
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(records, f)

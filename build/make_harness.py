"""LeetCode-style harness for every coding question: starter code + verified test cases.

Reads the built payload (site/data/questions.json), writes build/harness/harness.json, which
build_site_data.py merges in. Steps per question:
  1. take the published solution's Python, find the main function (or class) and its parameters;
  2. starter = the solution's imports + that signature with an empty body;
  3. record calls from matching build/solution_checks scripts (harness/capture.py);
  4. keep only cases the published solution reproduces (harness/validate.py).
Usage: python build/make_harness.py [--only ID]
"""
import ast
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / 'build/harness'
CAP = H / 'captures'
JOBS = H / 'jobs'
for d in (CAP, JOBS):
    d.mkdir(parents=True, exist_ok=True)
CHECKS = ROOT / 'build/solution_checks'
PY = sys.executable

qs = json.loads((ROOT / 'site/data/questions.json').read_text(encoding='utf-8'))['questions']
only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
coding = [q for q in qs if (q['type'] == 'coding' or q['subsection'] == 'ml-coding') and (not only or q['id'] == only)]


def blocks(q):
    return re.findall(r'```(?:python|py)\n([\s\S]*?)```', q.get('solution', ''))


def squash(name):
    return re.sub(r'[^a-z0-9]', '', (name or '').lower())


def pick_main(q, code):
    tree = ast.parse(code)
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    if not funcs:
        return tree, None, classes
    called = {c.func.id for f in funcs for c in ast.walk(f) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id != f.name}
    cands = [f for f in funcs if f.name not in called] or funcs
    sig = re.match(r'\s*(?:def\s+)?([A-Za-z_]\w*)', q.get('function_signature') or q.get('practice_signature') or '')
    want = squash(sig.group(1)) if sig else ''
    match = [f for f in cands if want and squash(f.name) == want]
    return tree, (match or cands)[-1], classes


def starter_for(tree, fn, classes):
    imports = [ast.unparse(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    head = '\n'.join(imports) + ('\n\n\n' if imports else '')
    if fn is not None:
        ret = f' -> {ast.unparse(fn.returns)}' if fn.returns else ''
        return f'{head}def {fn.name}({ast.unparse(fn.args)}){ret}:\n    # Write your solution here.\n    pass\n'
    out = []
    for c in classes:
        lines = [f'class {c.name}:']
        for m in c.body:
            if isinstance(m, ast.FunctionDef):
                lines.append(f'    def {m.name}({ast.unparse(m.args)}):\n        pass\n')
        out.append('\n'.join(lines) if len(lines) > 1 else lines[0] + '\n    pass\n')
    return head + '\n\n'.join(out)


# Index check scripts: function name -> [(script, normalized body)].
script_funcs = {}
for s in CHECKS.glob('*.py'):
    try:
        t = ast.parse(s.read_text(encoding='utf-8'))
    except Exception:
        continue
    for n in t.body:
        if isinstance(n, ast.FunctionDef):
            script_funcs.setdefault(n.name, []).append((s, ast.dump(ast.Module(body=n.body, type_ignores=[]))))


def candidate_scripts(q, fn):
    found = []
    if q['id'].startswith('curated-local-'):
        key = q['id'][len('curated-local-'):]
        for name in (key, 'old-' + key):
            p = CHECKS / f'{name}.py'
            if p.exists():
                found.append(p)
    body = ast.dump(ast.Module(body=fn.body, type_ignores=[]))
    found += [s for s, b in script_funcs.get(fn.name, []) if b == body]
    return list(dict.fromkeys(found))


def capture(script):
    out = CAP / (script.stem + '.json')
    if out.exists() and out.stat().st_mtime >= script.stat().st_mtime:
        return out
    try:
        subprocess.run([PY, str(H / 'capture.py'), str(script), str(out)], cwd=str(CHECKS), timeout=120,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        pass
    return out if out.exists() else None


plans = []
for q in coding:
    if q.get('checker'):
        continue  # keep the hand-written practice checks
    bl = blocks(q)
    if not bl:
        plans.append((q, None, 'no solution code'))
        continue
    code = bl[0]
    try:
        tree, fn, classes = pick_main(q, code)
    except SyntaxError:
        plans.append((q, None, 'solution code does not parse'))
        continue
    starter = starter_for(tree, fn, classes)
    if fn is None:
        plans.append((q, {'starter': starter}, 'class-based: starter only'))
        continue
    params = [a.arg for a in fn.args.args]
    plans.append((q, {'starter': starter, 'function': fn.name, 'params': params, 'code': code,
                      'scripts': candidate_scripts(q, fn)}, None))

scripts = sorted({s for _, p, _ in plans if p and 'scripts' in p for s in p['scripts']})
print(f'{len(plans)} coding questions without practice checks; capturing {len(scripts)} check scripts…', flush=True)
with ThreadPoolExecutor(6) as pool:
    cap_paths = dict(zip(scripts, pool.map(capture, scripts)))


def validate(item):
    q, p, why = item
    if not p or 'function' not in p:
        return q['id'], p, why
    caps = []
    for s in p['scripts']:
        path = cap_paths.get(s)
        if path:
            names = [k for k, v in json.loads(path.read_text(encoding='utf-8')).items() if isinstance(v, list) and v and len(v[0]['args']) == len(p['params'])]
            caps += [{'function': n, 'path': str(path)} for n in names]
    job = JOBS / (re.sub(r'[^\w-]', '_', q['id']) + '.json')
    out = job.with_suffix('.out.json')
    job.write_text(json.dumps({'code': p['code'], 'function': p['function'], 'params': p['params'],
                               'examples': q.get('examples') or [], 'captures': caps}), encoding='utf-8')
    try:
        r = subprocess.run([PY, str(H / 'validate.py'), str(job), str(out)], timeout=180, capture_output=True, text=True)
        if r.returncode:
            return q['id'], {'starter': p['starter'], 'function': p['function'], 'params': p['params']}, 'validate failed: ' + r.stderr.strip().splitlines()[-1][:120]
    except subprocess.TimeoutExpired:
        return q['id'], {'starter': p['starter'], 'function': p['function'], 'params': p['params']}, 'validate timed out'
    res = json.loads(out.read_text(encoding='utf-8'))
    entry = {'starter': p['starter'], 'function': p['function'], 'params': p['params']}
    if res['cases']:
        entry.update(cases=res['cases'], samples=res['samples'], numpy=res['numpy'])
    return q['id'], entry, json.dumps(res['report'])


with ThreadPoolExecutor(6) as pool:
    results = list(pool.map(validate, plans))

harness, stats = {}, {'tests': 0, 'starter only': 0, 'nothing': 0}
for qid, entry, why in results:
    if entry:
        harness[qid] = entry
        stats['tests' if entry.get('cases') else 'starter only'] += 1
    else:
        stats['nothing'] += 1
    if not entry or not entry.get('cases'):
        print(f'  no tests: {qid}: {why}')
path = H / 'harness.json'
old = json.loads(path.read_text(encoding='utf-8')) if only and path.exists() else {}
old.update(harness)
path.write_text(json.dumps(old, ensure_ascii=False), encoding='utf-8')
print('summary:', stats, '| total cases:', sum(len(e.get('cases', [])) for e in harness.values()))

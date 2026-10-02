/* Runs ONLY inside the visitor's browser. Worker termination stops runaway code. */
importScripts('pyodide/pyodide.js');
let py;
async function init(){
  try{
    postMessage({type:'status',message:'Loading local Python runtime…'});
    py=await loadPyodide({indexURL:'pyodide/'});
    postMessage({type:'status',message:'Loading NumPy…'});
    await py.loadPackage('numpy');
    py.runPython(`
import io as _atlas_io, sys as _atlas_sys, json as _atlas_json, traceback as _atlas_traceback, math as _atlas_math
class _AtlasOutput(_atlas_io.StringIO):
    def write(self, s):
        if self.tell() + len(s) > 65536:
            raise RuntimeError('Output limit exceeded (64 KB).')
        return super().write(s)
import copy as _atlas_copy
def _atlas_dec(v):
    if isinstance(v, dict) and '__nd__' in v:
        import numpy as np
        return np.array(_atlas_dec(v['__nd__']), dtype=v.get('dtype'))
    if isinstance(v, list):
        return [_atlas_dec(x) for x in v]
    if isinstance(v, dict):
        return {k: _atlas_dec(x) for k, x in v.items()}
    return v
def _atlas_norm(v):
    if type(v).__module__ == 'numpy':
        v = v.tolist()
    if isinstance(v, tuple):
        v = list(v)
    if isinstance(v, list):
        return [_atlas_norm(x) for x in v]
    if isinstance(v, dict):
        return {k: _atlas_norm(x) for k, x in v.items()}
    return v
def _atlas_equal(a, b):
    a, b = _atlas_norm(a), _atlas_norm(b)
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return _atlas_math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-8)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_atlas_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_atlas_equal(a[k], b[k]) for k in a)
    return a == b
def _atlas_repr(v):
    s = repr(_atlas_norm(v))
    return s if len(s) <= 800 else s[:800] + ' …'
def _atlas_execute(code, stdin, checker_json, mode):
    old_in, old_out, old_err = _atlas_sys.stdin, _atlas_sys.stdout, _atlas_sys.stderr
    out = _AtlasOutput()
    namespace = {'__name__': '__main__'}
    try:
        _atlas_sys.stdin = _atlas_io.StringIO(stdin)
        _atlas_sys.stdout = _atlas_sys.stderr = out
        exec(compile(code, '<solution>', 'exec'), namespace)
        checker = _atlas_json.loads(checker_json)
        if checker is None or mode == 'script':
            return _atlas_json.dumps({'output': out.getvalue()})
        function = namespace.get(checker['function'])
        if not callable(function):
            raise ValueError('Define the function ' + checker['function'] + '(...) to run the test cases.')
        cases = checker['cases']
        if mode == 'run':
            cases = cases[:max(1, checker.get('samples') or len(cases))]
        params = checker.get('params') or []
        results, passed_count = [], 0
        for i, case in enumerate(cases):
            args = _atlas_dec(case.get('args', []))
            expected = _atlas_dec(case['expected'])
            buf = _AtlasOutput()
            _atlas_sys.stdout = _atlas_sys.stderr = buf
            got, error = None, None
            try:
                got = function(*_atlas_copy.deepcopy(args))
                ok = _atlas_equal(got, expected)
            except Exception:
                ok, error = False, _atlas_traceback.format_exc().split('File "<solution>"', 1)[-1][-1500:]
            finally:
                _atlas_sys.stdout = _atlas_sys.stderr = out
            passed_count += ok
            row = {'case': i + 1, 'passed': ok, 'input': [[params[j] if j < len(params) else 'arg' + str(j + 1), _atlas_repr(a)] for j, a in enumerate(args)],
                   'expected': _atlas_repr(expected), 'got': None if error else _atlas_repr(got), 'stdout': buf.getvalue()[:2000], 'error': error}
            if mode == 'run':
                results.append(row)
            elif not ok:
                results.append(row)
                break   # like an online judge: report the first failing case
        return _atlas_json.dumps({'mode': mode, 'total': len(checker['cases']) if mode == 'submit' else len(cases), 'passed_count': passed_count,
                                  'results': results, 'passed': passed_count == len(cases) and not (mode == 'submit' and results), 'output': out.getvalue()})
    except BaseException:
        return _atlas_json.dumps({'error': out.getvalue() + _atlas_traceback.format_exc()})
    finally:
        _atlas_sys.stdin, _atlas_sys.stdout, _atlas_sys.stderr = old_in, old_out, old_err
`);
    postMessage({type:'ready'});
  }catch(e){postMessage({type:'init-error',error:e.message})}
}
const ready=init();
self.onmessage=async({data})=>{
  await ready;const start=performance.now();
  try{
    const execute=py.globals.get('_atlas_execute');
    const result=JSON.parse(execute(data.code,data.stdin,JSON.stringify(data.checker||null),data.mode||(data.checker?'submit':'script')));execute.destroy();
    postMessage({type:'result',id:data.id,...result,elapsed:performance.now()-start});
  }catch(e){postMessage({type:'result',id:data.id,error:e.message,elapsed:performance.now()-start})}
};

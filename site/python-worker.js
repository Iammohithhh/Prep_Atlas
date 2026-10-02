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
def _atlas_execute(code, stdin, checker_json):
    old_in, old_out, old_err = _atlas_sys.stdin, _atlas_sys.stdout, _atlas_sys.stderr
    out = _AtlasOutput()
    namespace = {'__name__': '__main__'}
    try:
        _atlas_sys.stdin = _atlas_io.StringIO(stdin)
        _atlas_sys.stdout = _atlas_sys.stderr = out
        exec(compile(code, '<solution>', 'exec'), namespace)
        checker = _atlas_json.loads(checker_json)
        if checker is None:
            return _atlas_json.dumps({'output': out.getvalue()})
        function = namespace.get(checker['function'])
        if not callable(function):
            raise ValueError('Implement the function ' + checker['function'] + ' to run solution checks.')
        failures = []
        total = len(checker['cases'])
        for i, case in enumerate(checker['cases']):
            args = case.get('args', [])
            got = function(*args)
            expected = case['expected']
            if checker.get('numpy'):
                import numpy as np
                try:
                    equal = np.shape(got) == np.shape(expected) and np.allclose(got, expected, rtol=1e-5, atol=1e-7)
                except (ValueError, TypeError):
                    equal = False
            elif checker.get('float'):
                equal = isinstance(got, (int, float)) and _atlas_math.isclose(got, expected, rel_tol=1e-6, abs_tol=1e-8)
            else:
                equal = got == expected
            if not equal:
                failures.append('Case ' + str(i + 1) + ': input ' + repr(args)[:240] + '\\n  expected: ' + repr(expected)[:240] + '\\n  received: ' + repr(got)[:240])
        summary = str(total - len(failures)) + '/' + str(total) + ' practice checks passed.'
        if failures:
            summary += '\\n\\n' + '\\n\\n'.join(failures[:5])
        return _atlas_json.dumps({'output': summary, 'passed': not failures})
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
    const result=JSON.parse(execute(data.code,data.stdin,JSON.stringify(data.checker||null)));execute.destroy();
    postMessage({type:'result',id:data.id,...result,elapsed:performance.now()-start});
  }catch(e){postMessage({type:'result',id:data.id,error:e.message,elapsed:performance.now()-start})}
};

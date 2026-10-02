"""Browser regressions for cold-worker cancellation, timeout and backup merging."""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from practice import make_practice

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/qa'
OUT.mkdir(exist_ok=True)
BASE = 'http://127.0.0.1:8765'
STORAGE = 'prep-atlas-progress-v1'
practice, references = make_practice()
questions = json.loads((ROOT / 'site/data/questions.json').read_text(encoding='utf-8'))['questions']
by_function = {q['checker']['function']: q for q in questions if q.get('checker')}


def finish(page, status, timeout=120000):
    page.wait_for_function('(status) => document.querySelector("#runtime-status").textContent === status', arg=status, timeout=timeout)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width':1440, 'height':1000})
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(BASE + '/#question/practice-stable-softmax')
    page.locator('#code-editor.ace_editor').wait_for()
    page.evaluate("editor.setValue('print(42)', -1)")
    page.locator('#run-code').click()
    assert page.evaluate('initReject !== null'), 'The first worker must still be loading'
    # Restart in the same JS turn: rejection from the cancelled run settles later.
    page.evaluate("stopWorker('Execution stopped.'); runCode(false)")
    finish(page, 'Run complete')
    assert page.locator('#output').inner_text().strip() == '42'
    print('PASS: cancelled during cold startup; immediate restart completed', flush=True)

    page.evaluate("editor.setValue('while True:\\n    pass', -1)")
    started = time.monotonic()
    page.locator('#run-code').click()
    finish(page, 'Stopped', timeout=20000)
    elapsed = time.monotonic() - started
    assert 9.5 <= elapsed < 16, elapsed
    assert page.locator('#output').inner_text() == 'Time limit exceeded (10 seconds).'
    assert page.locator('#run-code').is_enabled()
    page.evaluate("editor.setValue('print(73)', -1)")
    page.locator('#run-code').click()
    finish(page, 'Run complete')
    assert page.locator('#output').inner_text().strip() == '73'
    print(f'PASS: actual timeout after {elapsed:.2f}s and worker recovery', flush=True)

    cases = 0
    for exercise in practice:
        q = by_function[exercise['checker']['function']]
        page.goto(BASE + '/#question/' + q['id'])
        page.locator('#code-editor.ace_editor').wait_for()
        page.evaluate('code => editor.setValue(code, -1)', references[exercise['id']])
        page.locator('#check-code').click()
        finish(page, 'Practice checks passed', timeout=30000)
        n = len(exercise['checker']['cases'])
        assert page.locator('#output').inner_text().startswith(f'{n}/{n} practice checks passed.')
        assert page.locator('[data-status]').input_value() == 'solved'
        cases += n
    print(f'PASS: all {len(practice)} browser reference solutions, {cases} cases', flush=True)

    ids = [by_function[practice[i]['checker']['function']]['id'] for i in range(3)]
    local = {ids[0]: {'notes':'newer local', 'updated':2000}, ids[1]: {'notes':'old local', 'code':'keep code', 'updated':1000}}
    page.evaluate('([key, value]) => localStorage.setItem(key, JSON.stringify(value))', [STORAGE, local])
    page.reload(); page.locator('#code-editor.ace_editor').wait_for()
    incoming = {'format':'prep-atlas', 'version':1, 'progress':{
        ids[0]: {'notes':'older incoming', 'updated':1000},
        ids[1]: {'notes':'new incoming <script>alert(1)</script>', 'updated':2000, 'status':'revisit'},
        ids[2]: {'notes':'new record', 'updated':1500, 'status':'solved'},
        'unknown-question-id': {'notes':'ignore', 'updated':9999},
    }}
    page.locator('#import-file').set_input_files({'name':'backup.json', 'mimeType':'application/json', 'buffer':json.dumps(incoming).encode()})
    page.wait_for_function("document.querySelector('#toast').textContent.includes('2 question records imported')")
    merged = page.evaluate('key => JSON.parse(localStorage.getItem(key))', STORAGE)
    assert merged[ids[0]] == local[ids[0]]
    assert merged[ids[1]]['notes'] == incoming['progress'][ids[1]]['notes']
    assert merged[ids[1]]['code'] == 'keep code'
    assert merged[ids[2]]['status'] == 'solved'
    assert 'unknown-question-id' not in merged
    with page.expect_download() as download:
        page.locator('#backup').click()
    download.value.save_as(str(OUT / 'edge-progress-backup.json'))
    assert json.loads((OUT / 'edge-progress-backup.json').read_text())['progress'] == merged
    page.locator('#import-file').set_input_files({'name':'bad.json', 'mimeType':'application/json', 'buffer':b'{"format":"wrong","progress":{}}'})
    page.wait_for_function("document.querySelector('#toast').textContent.includes('not a valid')")
    assert page.evaluate('key => JSON.parse(localStorage.getItem(key))', STORAGE) == merged
    print('PASS: import keeps newer local records, merges valid fields, ignores unknown IDs, exports intact and rejects invalid format', flush=True)

    mobile = browser.new_context(viewport={'width':390, 'height':844}, is_mobile=True, has_touch=True)
    mp = mobile.new_page()
    for route, screenshot in [('overview', 'overview-mobile.png'), ('dsa', 'questions-mobile.png')]:
        mp.goto(BASE + '/#' + route)
        mp.locator('h1').wait_for()
        mp.evaluate('document.fonts.ready')
        mp.wait_for_timeout(250)
        overflow = mp.evaluate("""() => ({width:innerWidth, scroll:document.documentElement.scrollWidth, elements:[...document.querySelectorAll('main *')].filter(e => (!e.closest('.table-wrap, .topic-strip') || e.matches('.table-wrap, .topic-strip')) && e.getBoundingClientRect().right > innerWidth + 1).slice(0,12).map(e => ({tag:e.tagName, cls:e.className, right:e.getBoundingClientRect().right}))})""")
        assert overflow['scroll'] <= overflow['width'] and not overflow['elements'], overflow
        mp.screenshot(path=str(OUT / screenshot), full_page=True)
    assert not errors, errors
    browser.close()
print('PASS: edge regressions and settled mobile layouts')

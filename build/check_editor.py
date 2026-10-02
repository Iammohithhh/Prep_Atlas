"""Browser check of the LeetCode-style flow. Usage: python build/check_editor.py [base_url]"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765'
ROOT = Path(__file__).resolve().parents[1]
qs = json.loads((ROOT / 'site/data/questions.json').read_text(encoding='utf-8'))['questions']
numpy_q = next(q for q in qs if q.get('checker', {}).get('numpy') and q['checker'].get('source') == 'generated')
STATUS = "s => ['Examples passed','Some examples failed','Accepted','Wrong answer','Error','Run complete','Ready to retry'].includes(document.querySelector('#runtime-status').textContent)"


def status(pg):
    pg.wait_for_function(STATUS, arg=None, timeout=120000)
    return pg.locator('#runtime-status').inner_text()


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 1000})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    for qid in ('b04_gameskraft_misc-002', numpy_q['id']):
        pg.goto(f'{BASE}/#question/{qid}')
        pg.locator('#run-code').wait_for()
        starter = pg.evaluate('editor.getValue()')
        print(f'\n[{qid}] starter first def:', next((l for l in starter.splitlines() if l.startswith('def ')), '?'))
        pg.click('#run-code'); s1 = status(pg)
        pg.click('#tab-solution')
        if pg.locator('#reveal-solution').count():
            pg.click('#reveal-solution')
        pg.click('#load-solution'); pg.click('#load-solution')
        pg.click('#run-code'); s2 = status(pg)
        if qid == 'b04_gameskraft_misc-002':
            pg.screenshot(path=str(ROOT / 'build/qa/redesign/run-examples.png'))
        pg.click('#check-code'); s3 = status(pg)
        print(f'  starter Run -> {s1} | solution Run -> {s2} | Submit -> {s3}')
        print('  ', pg.locator('#output .verdict').first.inner_text())
    pg.screenshot(path=str(ROOT / 'build/qa/redesign/submit.png'))
    print('page errors:', errs or 'none')
    b.close()

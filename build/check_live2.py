"""Reproduce: open the k-th greatest prefix question, load its solution into the editor, Run, then Check."""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'https://placement-atlas.vercel.app'
DONE = "['Run complete','Execution error','Ready to retry','Practice checks passed','Review failing cases'].includes(document.querySelector('#runtime-status').textContent)"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    logs = []
    pg.on('pageerror', lambda e: logs.append('pageerror: ' + str(e)))
    pg.on('console', lambda m: logs.append(f'console.{m.type}: {m.text}'))
    pg.goto(BASE + '/#question/b04_gameskraft_misc-001')
    pg.locator('#run-code').wait_for()
    pg.click('#tab-solution')
    if pg.locator('#reveal-solution').count():
        pg.click('#reveal-solution')
    pg.click('#load-solution'); pg.click('#load-solution')
    for action in ('#run-code', '#check-code'):
        pg.click(action)
        pg.wait_for_function(DONE, timeout=120000)
        print(action, '->', pg.locator('#runtime-status').inner_text(), '|', pg.locator('#output').inner_text()[:400].replace('\n', ' / '))
    print('\n'.join(logs[-15:]) or 'no console output')
    b.close()

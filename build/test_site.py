"""Meaningful browser integration checks for storage, filtering and execution."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from practice import make_practice
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/qa';OUT.mkdir(exist_ok=True)
data=json.loads((ROOT/'site/data/questions.json').read_text(encoding='utf-8'))
_,refs=make_practice()

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000})
    page=context.new_page();errors=[]
    page.on('pageerror',lambda err:errors.append(str(err)))
    page.goto('http://127.0.0.1:8765');page.locator('h1').wait_for()
    assert page.get_by_text('Placement, one pattern at a time.',exact=True).is_visible()
    page.screenshot(path=str(OUT/'overview-light.png'),full_page=True)
    page.locator('#theme').select_option('dark')
    assert page.locator('html').get_attribute('data-theme')=='dark'
    page.screenshot(path=str(OUT/'overview-dark.png'),full_page=True)
    page.locator('#theme').select_option('light')
    page.goto('http://127.0.0.1:8765/#dsa')
    page.locator('#search').fill('histogram')
    assert page.locator('.question-list-row').count()>=1
    assert 'histogram' in page.locator('#question-results').inner_text().lower()
    page.locator('#filter-company').select_option('Google')
    assert page.locator('.question-list-row').count()==0
    page.locator('#clear-filters').click()
    assert page.locator('.question-list-row').count()>0
    page.goto('http://127.0.0.1:8765/#question/practice-stable-softmax')
    page.locator('#code-editor.ace_editor').wait_for()
    page.locator('#tab-notes').click();page.locator('#notes').fill('Subtract max before exp. <script>alert(1)</script>')
    page.reload();page.locator('#tab-notes').click()
    assert page.locator('#notes').input_value()=='Subtract max before exp. <script>alert(1)</script>'
    page.locator('#tab-problem').click()
    page.evaluate("code=>editor.setValue(code,-1)", 'import numpy as np\nprint(np.array([1, 2, 3]).sum())\nprint(input())')
    page.locator('.custom-input summary').click()
    page.locator('#stdin').fill('hello atlas')
    page.locator('#run-script').click()
    page.wait_for_function("document.querySelector('#runtime-status').textContent === 'Run complete'",timeout=120000)
    assert page.locator('#output').inner_text().strip()=='6\nhello atlas'
    page.evaluate("code=>editor.setValue(code,-1)",refs['practice-stable-softmax'])
    page.locator('#check-code').click()
    page.wait_for_function("document.querySelector('#runtime-status').textContent === 'Accepted'",timeout=30000)
    assert page.locator('[data-status]').input_value()=='solved'
    page.screenshot(path=str(OUT/'python-checks.png'),full_page=True)
    page.evaluate("code=>editor.setValue(code,-1)",'def stable_softmax(logits):\n    return [[0]]')
    page.locator('#check-code').click()
    page.wait_for_function("document.querySelector('#runtime-status').textContent === 'Wrong answer'",timeout=30000)
    assert '0 / 4 test cases passed' in page.locator('#output').inner_text()
    page.evaluate("code=>editor.setValue(code,-1)",'print(1/0)')
    page.locator('#run-code').click()
    page.wait_for_function("document.querySelector('#runtime-status').textContent === 'Error'",timeout=30000)
    assert 'ZeroDivisionError' in page.locator('#output').inner_text()
    page.evaluate("code=>editor.setValue(code,-1)",'while True:\n    pass')
    page.locator('#run-code').click()
    page.wait_for_function("document.querySelector('#runtime-status').textContent === 'Running…'")
    page.locator('#stop-code').click()
    assert 'stopped' in page.locator('#output').inner_text().lower()
    page.goto('http://127.0.0.1:8765/#progress')
    assert page.get_by_text('Numerically stable row-wise softmax',exact=True).is_visible()
    with page.expect_download() as download:
        page.locator('#backup').click()
    download.value.save_as(str(OUT/'progress-backup.json'))
    backup=json.loads((OUT/'progress-backup.json').read_text())
    assert backup['progress']['practice-stable-softmax']['notes'].startswith('Subtract')
    page.goto('http://127.0.0.1:8765/#trends');page.locator('[data-report]').first.click()
    page.locator('#report-body').get_by_role('heading',name='Trends',exact=True).wait_for()
    page.goto('http://127.0.0.1:8765/#coverage')
    assert page.locator('.coverage-table tbody tr').count()==52
    assert not errors,errors
    # Browser-independent storage and mobile layout.
    mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    mp=mobile.new_page();mp.goto('http://127.0.0.1:8765');mp.locator('h1').wait_for()
    assert mp.locator('#sidebar-progress').inner_text().startswith('Your progress\n0 /')
    mp.evaluate('document.fonts.ready')
    mp.wait_for_timeout(250)
    assert mp.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    assert mp.evaluate("[...document.querySelectorAll('main *')].filter(e => !e.closest('.table-wrap') || e.matches('.table-wrap')).every(e => e.getBoundingClientRect().right <= innerWidth + 1)")
    mp.screenshot(path=str(OUT/'overview-mobile.png'),full_page=True)
    mp.locator('#menu').click();assert mp.locator('#menu').get_attribute('aria-expanded')=='true'
    mp.locator('#nav').get_by_role('link',name='DSA',exact=False).click();mp.locator('#search').wait_for()
    mp.wait_for_function("(s => getComputedStyle(s).transform === `matrix(1, 0, 0, 1, -${s.offsetWidth}, 0)`)(document.querySelector('#sidebar'))")
    mp.screenshot(path=str(OUT/'questions-mobile.png'),full_page=True)
    browser.close()
print('PASS: filters, themes, notes, isolated progress, Python/NumPy, solution checks, wrong answers, errors, stop, backup, research, coverage and mobile layout.')

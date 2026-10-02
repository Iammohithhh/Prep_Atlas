"""Smoke-test the deployed site: load a coding question, run Python + NumPy. Usage: python build/check_live.py [base_url]"""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'https://placement-atlas.vercel.app'
DONE = "['Run complete','Execution error','Ready to retry'].includes(document.querySelector('#runtime-status').textContent)"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(BASE + '/#question/b08_devrev_trilogy_amzn_atl-006')
    pg.locator('#run-code').wait_for()
    pg.evaluate('c => editor.setValue(c, -1)', 'import numpy as np\nprint(sum(range(10)), np.arange(3).tolist())')
    pg.click('#run-code')
    pg.wait_for_function(DONE, timeout=120000)
    print('status:', pg.locator('#runtime-status').inner_text())
    print('output:', pg.locator('#output').inner_text())
    print('page errors:', errs or 'none')
    b.close()

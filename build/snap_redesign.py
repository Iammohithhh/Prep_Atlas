"""Screenshots of key views (desktop + phone, light + dark) into build/qa/redesign/. Needs serve.py on :8765."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/qa/redesign'
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'http://127.0.0.1:8765/'
qs = json.loads((ROOT / 'site/data/questions.json').read_text(encoding='utf-8'))['questions']
coding = next(q for q in qs if q.get('checker'))
mcq = next(q for q in qs if q.get('options') and q['origin'] == 'local')
views = [('overview', '#overview'), ('dsa', '#dsa'), ('coding', '#question/' + coding['id']), ('mcq', '#question/' + mcq['id'])]
only = set(sys.argv[1:])

with sync_playwright() as p:
    b = p.chromium.launch()
    errors = []
    for scheme in ('light', 'dark'):
        for device, size in (('desk', {'width': 1440, 'height': 900}), ('phone', {'width': 390, 'height': 844})):
            ctx = b.new_context(viewport=size, color_scheme=scheme)
            page = ctx.new_page()
            page.on('pageerror', lambda e: errors.append(str(e)))
            for name, h in views:
                if only and name not in only:
                    continue
                page.goto(BASE + h)
                page.wait_for_timeout(700)
                if name == 'mcq':
                    page.locator('.mcq-option').first.click()
                    page.click('#check-answer')
                    page.wait_for_timeout(200)
                page.screenshot(path=str(OUT / f'{name}-{device}-{scheme}.png'), full_page=(device == 'desk' and name != 'coding'))
                width = page.evaluate('document.documentElement.scrollWidth')
                if width > size['width'] + 1:
                    errors.append(f'{name}-{device}: horizontal overflow {width}px')
            ctx.close()
    b.close()
print('errors:', errors or 'none')

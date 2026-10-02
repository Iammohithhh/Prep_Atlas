"""Scan files that git would commit for personal-data patterns. Usage: python build/scan_pii.py"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
files = subprocess.run(['git', 'add', '-A', '--dry-run'], cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
paths = [ROOT / re.sub(r"^add '(.*)'$", r'\1', f) for f in files]
EMAIL = re.compile(r'\b[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[a-zA-Z]{2,}\b')
PHONE = re.compile(r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)')
IDS = re.compile(r'(?i)\b(roll\s*(no|number)|candidate\s*id|application\s*id|registration\s*no)\b')
ALLOWED_EMAILS = {'noreply@anthropic.com'}
hits = 0
for p in paths:
    if p.suffix.lower() in {'.wasm', '.whl', '.zip', '.woff2', '.png', '.jpg', '.ico'} or 'pyodide' in p.parts or 'vendor' in p.parts:
        continue
    try:
        text = p.read_text(encoding='utf-8')
    except (UnicodeDecodeError, OSError):
        continue
    for name, rx in (('email', EMAIL), ('phone', PHONE), ('id', IDS)):
        for m in set(rx.findall(text) if name != 'id' else [x[0] for x in rx.findall(text)]):
            if name == 'email' and (m in ALLOWED_EMAILS or 'hackerrank.com' in m or m in {'julia@gmail.com', 'a7_1@baddomain.com'}):
                continue
            hits += 1
            print(f'{name:5s} {p.relative_to(ROOT)}: {m}')
print('hits:', hits)

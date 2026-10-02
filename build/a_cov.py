"""Worker A: coverage including alias entries (coverage.py ignores them)."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'build/manifest.json').read_text(encoding='utf-8'))
done = set()
for path in (ROOT / 'build/raw').glob('*.json'):
    data = json.loads(path.read_text(encoding='utf-8'))
    for q in data.get('questions', []):
        done.update(q.get('source_files', []))
    done.update(s['file'] for s in data.get('skipped_files', []))
    for a in data.get('aliases', []):
        done.update(a['source_files'])
if len(sys.argv) > 1:
    for f in manifest[sys.argv[1]]:
        if f not in done: print(f)
else:
    mine = 'IBM,Gameskraft,Uber,Google,Trilogy,PayPal,Dream11,Zscaler,Adobe,Salesforce,Flipkart,Cadence,UBS,Qualcomm,Oracle / Goldman Sachs'.split(',')
    t = 0
    for c in mine:
        n = sum(f not in done for f in manifest[c]); t += n
        print(f'{n:4d}/{len(manifest[c]):<4d} {c}')
    print('TOTAL', t)

"""Worker A: one-line digest of each uncovered file (alias-aware): python build/a_digest.py Company [width]"""
import json, re, sys, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'build/manifest.json').read_text(encoding='utf-8'))
done = set()
for path in (ROOT / 'build/raw').glob('*.json'):
    data = json.loads(path.read_text(encoding='utf-8'))
    for q in data.get('questions', []): done.update(q.get('source_files', []))
    done.update(s['file'] for s in data.get('skipped_files', []))
    for a in data.get('aliases', []): done.update(a['source_files'])
c = sys.argv[1]; w = int(sys.argv[2]) if len(sys.argv) > 2 else 160
for i, rel in enumerate(f for f in manifest[c] if f not in done):
    p = ROOT / 'build/ocr' / (hashlib.sha256(rel.encode('utf-8')).hexdigest()[:20] + '.json')
    t = json.loads(p.read_text(encoding='utf-8')).get('text', '') if p.exists() else '(no OCR)'
    t = re.sub(r'\s+', ' ', t)
    print(f'[{i}] {Path(rel).name} :: {t[:w]}')

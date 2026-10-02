"""Worker A: full compressed OCR text for uncovered files by digest index range: a_txt.py Company start end [maxchars]"""
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
c, s, e = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); mx = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
files = [f for f in manifest[c] if f not in done]
for i in range(s, min(e, len(files))):
    rel = files[i]
    p = ROOT / 'build/ocr' / (hashlib.sha256(rel.encode('utf-8')).hexdigest()[:20] + '.json')
    t = json.loads(p.read_text(encoding='utf-8')).get('text', '') if p.exists() else ''
    t = re.sub(r'\s+', ' ', t)
    print(f'[{i}] {Path(rel).name} :: {t[:mx]}\n')

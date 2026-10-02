"""Report which manifest files are not yet represented by a question or an explicit skip."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'build/manifest.json').read_text(encoding='utf-8'))


def covered_files():
    done = set()
    for path in (ROOT / 'build/raw').glob('*.json'):
        data = json.loads(path.read_text(encoding='utf-8'))
        for q in data.get('questions', []):
            done.update(q.get('source_files', []))
        done.update(s['file'] for s in data.get('skipped_files', []))
        for a in data.get('aliases', []):
            done.update(a['source_files'])
    return done


def remaining(company=None):
    done = covered_files()
    out = {}
    for c, files in manifest.items():
        if company and c != company:
            continue
        left = [f for f in files if f not in done]
        if left:
            out[c] = left
    return out


if __name__ == '__main__':
    left = remaining(sys.argv[1] if len(sys.argv) > 1 else None)
    if len(sys.argv) > 1:
        for f in next(iter(left.values()), []):
            print(f)
    else:
        for c, files in sorted(left.items(), key=lambda kv: -len(kv[1])):
            print(f'{len(files):4d}/{len(manifest[c]):<4d} {c}')
        print('TOTAL remaining:', sum(map(len, left.values())))

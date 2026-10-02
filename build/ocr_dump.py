"""Print OCR text for a company's not-yet-covered files, in manifest order.

Usage: python build/ocr_dump.py "Company" [--offset N] [--limit N] [--all]
OCR is a reading aid only; open the image itself whenever numbers, options or code look uncertain.
"""
import argparse
import hashlib
import json
from pathlib import Path

from coverage import manifest, remaining

ROOT = Path(__file__).resolve().parents[1]


def cache_path(rel):
    return ROOT / 'build/ocr' / (hashlib.sha256(rel.encode('utf-8')).hexdigest()[:20] + '.json')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('company')
    ap.add_argument('--offset', type=int, default=0)
    ap.add_argument('--limit', type=int, default=15)
    ap.add_argument('--all', action='store_true', help='include files already covered')
    a = ap.parse_args()
    files = manifest[a.company] if a.all else remaining(a.company).get(a.company, [])
    print(f'# {a.company}: {len(files)} files listed; showing {a.offset}..{a.offset + a.limit - 1}')
    for i, rel in enumerate(files[a.offset:a.offset + a.limit], start=a.offset):
        p = cache_path(rel)
        text = json.loads(p.read_text(encoding='utf-8')).get('text', '') if p.exists() else '(no OCR cache)'
        print(f'\n=== [{i}] {Path(rel).name}\nPATH: {ROOT / rel}\n{text.strip()[:4000]}')


if __name__ == '__main__':
    main()

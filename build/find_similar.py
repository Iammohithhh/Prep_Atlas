"""Search every existing question (all raw batches + web/practice in the built payload) by keywords.

Usage: python build/find_similar.py "word1 word2 ..."   -> best matches with id, company, section, title
Use it before adding a question, to apply the pattern-dedupe rule (alias/merge instead of re-adding).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load():
    seen = {}
    for path in sorted((ROOT / 'build/raw').glob('*.json')):
        for q in json.loads(path.read_text(encoding='utf-8')).get('questions', []):
            seen[q['id']] = q
    site = ROOT / 'site/data/questions.json'
    if site.exists():
        for q in json.loads(site.read_text(encoding='utf-8'))['questions']:
            seen.setdefault(q['id'], q)
    return list(seen.values())


def words(s):
    return set(re.findall(r'[a-z0-9]{3,}', s.lower()))


def main():
    query = words(' '.join(sys.argv[1:]))
    scored = []
    for q in load():
        text = ' '.join(str(q.get(k, '')) for k in ('title', 'statement', 'pattern', 'subsection'))
        hit = len(query & words(text))
        if hit:
            scored.append((hit, q))
    scored.sort(key=lambda t: -t[0])
    for hit, q in scored[:12]:
        print(f"{hit:2d}  {q['id']}  [{q.get('company')}|{q.get('section')}/{q.get('subsection')}]  {q['title']}")


if __name__ == '__main__':
    main()

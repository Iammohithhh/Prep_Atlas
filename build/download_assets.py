"""Fetch pinned browser assets. Run once; site works without CDNs afterwards."""
from pathlib import Path
from urllib.request import urlopen
import json
import io
import tarfile
ROOT = Path(__file__).resolve().parents[1] / 'site' / 'vendor'
ASSETS = {
    'marked.js': 'https://cdn.jsdelivr.net/npm/marked@15.0.12/marked.min.js',
    'purify.js': 'https://cdn.jsdelivr.net/npm/dompurify@3.2.6/dist/purify.min.js',
    'ace.js': 'https://cdn.jsdelivr.net/npm/ace-builds@1.43.3/src-min-noconflict/ace.js',
    'mode-python.js': 'https://cdn.jsdelivr.net/npm/ace-builds@1.43.3/src-min-noconflict/mode-python.js',
    'theme-tomorrow.js': 'https://cdn.jsdelivr.net/npm/ace-builds@1.43.3/src-min-noconflict/theme-tomorrow.js',
    'theme-tomorrow_night.js': 'https://cdn.jsdelivr.net/npm/ace-builds@1.43.3/src-min-noconflict/theme-tomorrow_night.js',
}
ROOT.mkdir(exist_ok=True)
for name, url in ASSETS.items():
    dest = ROOT / name
    if not dest.exists():
        with urlopen(url, timeout=60) as res:
            dest.write_bytes(res.read())
        print(name, dest.stat().st_size)
(ROOT / 'sources.json').write_text(json.dumps({**ASSETS,'katex/':'https://registry.npmjs.org/katex/-/katex-0.16.22.tgz'}, indent=2), encoding='utf-8')
katex=ROOT/'katex'
if not (katex/'katex.min.js').exists():
    with urlopen('https://registry.npmjs.org/katex/-/katex-0.16.22.tgz',timeout=60) as res:
        archive=tarfile.open(fileobj=io.BytesIO(res.read()),mode='r:gz')
    for member in archive.getmembers():
        prefix='package/dist/'
        if not member.isfile():continue
        if member.name.startswith(prefix):
            rel=member.name[len(prefix):]
            if rel in ['katex.min.js','katex.min.css'] or rel.startswith('fonts/'):
                target=katex/rel
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(archive.extractfile(member).read())
        elif member.name=='package/LICENSE':
            katex.mkdir(exist_ok=True)
            (katex/'LICENSE').write_bytes(archive.extractfile(member).read())
    print('KaTeX 0.16.22 and local fonts downloaded.')

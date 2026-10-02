"""Worker A utility: split a bundle file with '#### FILE <relpath under build/>' markers into files."""
import sys
from pathlib import Path
B = Path(__file__).resolve().parent
text = Path(sys.argv[1]).read_text(encoding='utf-8')
parts = text.split('#### FILE ')
for part in parts[1:]:
    head, _, body = part.partition('\n')
    p = B / head.strip()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body.rstrip('\n') + '\n', encoding='utf-8')
    print('wrote', p.name)

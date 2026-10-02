"""Private contact sheets for visual source review; never copied into site/."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('company')
parser.add_argument('--page-size', type=int, default=4)
parser.add_argument('--offset', type=int, default=0)
parser.add_argument('--limit', type=int)
args = parser.parse_args()
manifest = json.loads((ROOT / 'build/manifest.json').read_text(encoding='utf-8'))
paths = [ROOT / p for p in manifest[args.company] if Path(p).suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}]
paths = paths[args.offset:None if args.limit is None else args.offset+args.limit]
out = ROOT / 'build/qa/source-review'
out.mkdir(parents=True, exist_ok=True)
for start in range(0, len(paths), args.page_size):
    group = paths[start:start + args.page_size]
    sheet = Image.new('RGB', (2000, 1100 * ((len(group) + 1) // 2)), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(group):
        x, y = i % 2 * 1000, i // 2 * 1100
        draw.text((x + 8, y + 8), path.name, fill='black')
        with Image.open(path) as source:
            picture = ImageOps.exif_transpose(source).convert('RGB')
            picture.thumbnail((990, 1065))
            sheet.paste(picture, (x + 5, y + 30))
    dest = out / (args.company.replace('/', '-').replace(' ', '_') + f'-{(args.offset+start) // args.page_size + 1}.jpg')
    sheet.save(dest, quality=94)
    print(dest)

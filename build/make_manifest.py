"""Build a deduplicated manifest of OA source files for the selected companies."""
import hashlib
import json
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".pdf", ".docx", ".txt"}

# folder name (lowercase) -> canonical company name
FOLDERS = {
    # Tier 1
    "google": "Google", "microsoft": "Microsoft", "apple": "Apple", "uber oa": "Uber",
    "linkedin oa": "LinkedIn", "de shaw": "DE Shaw", "atlassian": "Atlassian", "adobe": "Adobe",
    "salesforce": "Salesforce", "devrev": "DevRev", "trilogy question": "Trilogy",
    # Tier 2
    "samsung srib": "Samsung SRIB", "qualcomm": "Qualcomm", "flipkart oa": "Flipkart",
    "myntra": "Myntra", "meesho sde": "Meesho", "phonepe": "PhonePe", "navi": "Navi",
    "grow": "Groww", "zepto": "Zepto", "dream 11": "Dream11", "gameskraft": "Gameskraft",
    "thoughtspot": "ThoughtSpot", "zscalar": "Zscaler", "motorq": "Motorq", "ui path": "UiPath",
    "amazon": "Amazon", "expedia": "Expedia", "visa": "Visa", "mastercard": "Mastercard",
    "paypal": "PayPal", "oracle and gs": "Oracle / Goldman Sachs", "cadence_pune": "Cadence",
    "texas": "Texas Instruments",
    # Tier 3
    "fractal": "Fractal", "sigmoid": "Sigmoid", "zs associates": "ZS Associates",
    "axtria inc. ( analyst)": "Axtria", "procdna": "ProcDNA", "maq": "MAQ Software",
    "hilabs": "HiLabs",
    # Finance / quant
    "pace stock": "Pace Stock Broking", "arpwood capital": "Arpwood Capital",
    "edelwiess": "Edelweiss", "ubs": "UBS", "deutsche bank": "Deutsche Bank",
    "bny melon": "BNY Mellon",
    # Extras
    "oracle": "Oracle", "sap lab": "SAP Labs", "ibm": "IBM",
    "ibm diversity hiring pool campus": "IBM", "ibm girls": "IBM", "hp": "HP", "turing": "Turing",
}


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    by_company = defaultdict(list)
    seen = set()
    for top in sorted(os.listdir(ROOT)):
        top_path = os.path.join(ROOT, top)
        if not os.path.isdir(top_path) or top in ("build", "research", "site"):
            continue
        for dirpath, dirnames, _ in os.walk(top_path):
            for d in sorted(dirnames):
                company = FOLDERS.get(d.lower())
                if not company:
                    continue
                for sub, _, files in os.walk(os.path.join(dirpath, d)):
                    for name in sorted(files):
                        if os.path.splitext(name)[1].lower() not in EXTS:
                            continue
                        path = os.path.join(sub, name)
                        digest = md5(path)
                        if digest in seen:
                            continue
                        seen.add(digest)
                        by_company[company].append(os.path.relpath(path, ROOT))
            # company folders are matched at any depth; don't descend into matched ones twice
            dirnames[:] = [d for d in dirnames if d.lower() not in FOLDERS]

    manifest = {c: sorted(set(p)) for c, p in sorted(by_company.items())}
    out = os.path.join(ROOT, "build", "manifest.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    total = sum(len(v) for v in manifest.values())
    for c, files in manifest.items():
        print(f"{len(files):5d}  {c}")
    print(f"{total:5d}  TOTAL across {len(manifest)} companies")
    missing = sorted(set(FOLDERS.values()) - set(manifest))
    print("No files:", ", ".join(missing))


if __name__ == "__main__":
    main()

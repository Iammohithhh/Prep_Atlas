"""Split manifest.json into transcription batches (one per agent)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

GROUPS = {
    "b01_oracle_a": [("Oracle", 0, 127)],
    "b02_oracle_b": [("Oracle", 127, None)],
    "b03_ibm": [("IBM", 0, None)],
    "b04_gameskraft_misc": ["Gameskraft", "Adobe", "Apple", "DE Shaw", "Visa", "Expedia",
                            "Qualcomm", "UBS", "Arpwood Capital", "Oracle / Goldman Sachs"],
    "b05_zs_fractal": ["ZS Associates", "Fractal"],
    "b06_sigmoid_procdna": ["Sigmoid", "ProcDNA"],
    "b07_google_uber_li_ms": ["Google", "Uber", "LinkedIn", "Microsoft"],
    "b08_devrev_trilogy_amzn_atl": ["DevRev", "Trilogy", "Amazon", "Atlassian"],
    "b09_axtria_maq_d11_paypal": ["Axtria", "MAQ Software", "Dream11", "PayPal"],
    "b10_mid_product": ["Zscaler", "SAP Labs", "HP", "PhonePe", "UiPath", "Deutsche Bank",
                        "Myntra", "Groww"],
    "b11_small": ["Texas Instruments", "Pace Stock Broking", "Meesho", "Flipkart", "Edelweiss",
                  "Salesforce", "ThoughtSpot", "Cadence", "BNY Mellon", "Mastercard", "Zepto",
                  "HiLabs", "Motorq"],
}


def main():
    manifest = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf-8"))
    os.makedirs(os.path.join(HERE, "batches"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "raw"), exist_ok=True)
    used = set()
    for key, items in GROUPS.items():
        batch = []
        for item in items:
            company, start, end = (item, 0, None) if isinstance(item, str) else item
            for path in manifest[company][start:end]:
                batch.append({"company": company, "file": path})
                used.add(path)
        with open(os.path.join(HERE, "batches", key + ".json"), "w", encoding="utf-8") as f:
            json.dump(batch, f, indent=1)
        print(f"{key}: {len(batch)} files")
    leftover = [p for files in manifest.values() for p in files if p not in used]
    print("unassigned:", len(leftover))


if __name__ == "__main__":
    main()

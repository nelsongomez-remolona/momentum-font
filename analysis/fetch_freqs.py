#!/usr/bin/env python3
"""Download real population allele frequencies from the Ensembl REST API
for the trait/ancestry SNPs discussed in this research thread, then analyze."""
import json, urllib.request, time, csv, sys

# Panel: rsID -> (gene, trait, highlight_allele, note)
# highlight_allele = the allele whose frequency tells the story.
PANEL = [
    ("rs671",      "ALDH2",      "Alcohol-flush ('Asian glow')",       "A", "A = deficient enzyme -> flushing"),
    ("rs1229984",  "ADH1B",      "Fast alcohol metabolism (His48Arg)", "A", "A = fast first-step metabolism"),
    ("rs3827760",  "EDAR",       "Thick straight hair / shovel teeth", "G", "G = derived V370A (East Asian)"),
    ("rs17822931", "ABCC11",     "Dry earwax / less body odor",        "T", "T = dry earwax (derived)"),
    ("rs4988235",  "LCT/MCM6",   "Lactase persistence (drink milk)",   "T", "T = keep digesting lactose as adult"),
    ("rs1815739",  "ACTN3",      "R577X 'sprint gene' (X=stop)",       "T", "T = X = nonfunctional alpha-actinin-3"),
]

# Columns to display: label -> 1000G phase_3 population code
# SE-Asian-adjacent proxies (nearest to Filipino) first, then super-populations.
COLS = [
    ("KHV (Vietnamese)", "KHV"),
    ("CDX (Dai)",        "CDX"),
    ("CHB (Han)",        "CHB"),
    ("JPT (Japanese)",   "JPT"),
    ("EAS (E Asian)",    "EAS"),
    ("SAS (S Asian)",    "SAS"),
    ("EUR (European)",   "EUR"),
    ("AFR (African)",    "AFR"),
    ("PEL (Peruvian)",   "PEL"),
]
COMP = {"A":"T","T":"A","C":"G","G":"C"}

def fetch(rsid, tries=4):
    url = f"https://rest.ensembl.org/variation/human/{rsid}?content-type=application/json;pops=1"
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=45) as r:
                return json.load(r)
        except Exception as e:
            if i == tries-1:
                raise
            time.sleep(2*(i+1))

def target_allele(data, allele):
    """Decide, globally for this SNP, which allele label to read (handles strand flips)."""
    seen = {p["allele"] for p in data.get("populations", []) if p["population"].startswith("1000GENOMES:phase_3")}
    if allele in seen:
        return allele
    c = COMP.get(allele)
    if c in seen:
        return c
    return allele

def freq_for(data, popcode, tgt):
    """Frequency of target allele in 1000GENOMES:phase_3:<popcode>.
    None only if the population was not genotyped; 0.0 if the allele is truly absent."""
    want = f"1000GENOMES:phase_3:{popcode}"
    entries = [p for p in data.get("populations", []) if p.get("population") == want]
    if not entries:
        return None
    alleles = {p["allele"]: p["frequency"] for p in entries}
    return alleles.get(tgt, 0.0)

rows = []
raw = {}
for rsid, gene, trait, allele, note in PANEL:
    print(f"fetching {rsid} ({gene})...", file=sys.stderr)
    d = fetch(rsid)
    raw[rsid] = d
    row = {"rsID": rsid, "gene": gene, "trait": trait, "allele": allele, "note": note}
    tgt = target_allele(d, allele)
    for label, code in COLS:
        f = freq_for(d, code, tgt)
        row[label] = round(f, 3) if f is not None else None
    rows.append(row)
    time.sleep(0.5)

# Save raw + tidy CSV
json.dump(raw, open("raw_variation.json", "w"))
with open("allele_frequencies.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    header = ["rsID","gene","trait","highlight_allele"] + [c[0] for c in COLS] + ["note"]
    w.writerow(header)
    for r in rows:
        w.writerow([r["rsID"],r["gene"],r["trait"],r["allele"]]+[r[c[0]] for c in COLS]+[r["note"]])

# Pretty console table
print("\n=== Highlight-allele frequency (1000 Genomes phase 3) ===\n")
h = f"{'gene':10} {'allele':6} " + " ".join(f"{c[0][:14]:>14}" for c in COLS)
print(h); print("-"*len(h))
for r in rows:
    line = f"{r['gene']:10} {r['allele']:6} " + " ".join(
        (f"{r[c[0]]*100:13.1f}%" if r[c[0]] is not None else f"{'n/a':>14}") for c in COLS)
    print(line)
print("\nSaved: allele_frequencies.csv, raw_variation.json")

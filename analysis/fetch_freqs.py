#!/usr/bin/env python3
"""Download real population allele frequencies from the Ensembl REST API
(1000 Genomes phase 3) for a comprehensive panel of trait / ancestry SNPs,
then tabulate. No API key required; Ensembl REST is open."""
import json, urllib.request, time, csv, sys

# category, rsID, gene, trait, highlight allele, note
PANEL = [
    ("Diet",       "rs4988235",  "LCT/MCM6", "Lactase persistence (drink milk)",   "T", "T = keep digesting lactose as adult (European variant)"),
    ("Diet",       "rs671",      "ALDH2",    "Alcohol flush ('Asian glow')",       "A", "A = deficient enzyme -> flushing"),
    ("Diet",       "rs1229984",  "ADH1B",    "Fast alcohol metabolism",            "A", "A = fast first-step metabolism"),
    ("Diet",       "rs174546",   "FADS1",    "Fatty-acid (PUFA) metabolism",       "T", "shown allele = one FADS1 diet-adaptation variant"),
    ("Pigment",    "rs1426654",  "SLC24A5",  "Light skin (West Eurasian)",         "A", "A = derived light-skin allele"),
    ("Pigment",    "rs16891982", "SLC45A2",  "Light skin (European)",              "G", "G = derived light-skin allele"),
    ("Pigment",    "rs12913832", "HERC2/OCA2","Blue eyes",                         "G", "G = derived blue-eye allele"),
    ("Morphology", "rs3827760",  "EDAR",     "Thick straight hair / shovel teeth", "G", "G = derived V370A (East Asian)"),
    ("Morphology", "rs17822931", "ABCC11",   "Dry earwax / less body odor",        "T", "T = dry earwax (derived)"),
    ("Disease",    "rs334",      "HBB",      "Sickle-cell (malaria resistance)",   "A", "A = HbS sickle allele"),
    ("Disease",    "rs2814778",  "ACKR1",    "Duffy-null (vivax-malaria resist.)", "C", "C = Duffy-negative"),
    ("Disease",    "rs73885319", "APOL1",    "APOL1 G1 (trypanosome resist.)",     "G", "G = African-specific G1 risk allele"),
    ("Physical",   "rs1815739",  "ACTN3",    "R577X 'sprint gene' (X=stop)",       "T", "T = X = nonfunctional alpha-actinin-3"),
    ("Pigment",    "rs1800414",  "OCA2",     "Light skin (EAST-Asian route)",      "C", "East-Asian-specific light-skin allele (His615Arg)"),
    ("Sensory",    "rs713598",   "TAS2R38",  "Bitter-taste (PTC) perception",      "G", "shown allele of the PTC taster/non-taster site"),
    ("Pharma",     "rs4244285",  "CYP2C19",  "CYP2C19*2 poor metabolizer",         "A", "A = *2 loss-of-function (clopidogrel etc.)"),
    ("Health",     "rs429358",   "APOE",     "APOE-e4 (Alzheimer risk allele)",    "C", "C = e4 risk allele"),
    ("Disease",    "rs601338",   "FUT2",     "FUT2 non-secretor (gut immunity)",   "A", "A = nonsense -> non-secretor"),
    ("Disease",    "rs1050828",  "G6PD",     "G6PD A- deficiency (malaria)",       "T", "T = African A- deficiency allele (X-linked)"),
]

# display label -> 1000G phase_3 code. SE-Asian (Filipino) proxies first.
COLS = [
    ("KHV (Viet~Fil)", "KHV"), ("CDX (Dai~Fil)", "CDX"),
    ("CHB (Han)", "CHB"), ("JPT (Japan)", "JPT"), ("EAS", "EAS"),
    ("SAS", "SAS"), ("EUR", "EUR"), ("AFR", "AFR"),
    ("YRI (Nigeria)", "YRI"), ("PEL (Peru)", "PEL"),
]
COMP = {"A":"T","T":"A","C":"G","G":"C"}

def fetch(rsid, tries=4):
    url = f"https://rest.ensembl.org/variation/human/{rsid}?content-type=application/json;pops=1"
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=45) as r:
                return json.load(r)
        except Exception:
            if i == tries-1: raise
            time.sleep(2*(i+1))

def target_allele(data, allele):
    seen = {p["allele"] for p in data.get("populations", []) if p["population"].startswith("1000GENOMES:phase_3")}
    if allele in seen: return allele
    c = COMP.get(allele)
    return c if c in seen else allele

def freq_for(data, popcode, tgt):
    want = f"1000GENOMES:phase_3:{popcode}"
    e = [p for p in data.get("populations", []) if p.get("population") == want]
    if not e: return None
    return {p["allele"]: p["frequency"] for p in e}.get(tgt, 0.0)

rows, raw = [], {}
for cat, rsid, gene, trait, allele, note in PANEL:
    print(f"fetching {rsid} ({gene})...", file=sys.stderr)
    d = fetch(rsid); raw[rsid] = d
    tgt = target_allele(d, allele)
    row = {"category":cat,"rsID":rsid,"gene":gene,"trait":trait,"allele":allele,"note":note}
    for label, code in COLS:
        f = freq_for(d, code, tgt)
        row[label] = round(f,3) if f is not None else None
    rows.append(row); time.sleep(0.4)

json.dump(raw, open("raw_variation.json","w"))
with open("allele_frequencies.csv","w",newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["category","rsID","gene","trait","highlight_allele"]+[c[0] for c in COLS]+["note"])
    for r in rows:
        w.writerow([r["category"],r["rsID"],r["gene"],r["trait"],r["allele"]]+[r[c[0]] for c in COLS]+[r["note"]])

print(f"\n=== {len(rows)} SNPs x {len(COLS)} populations (1000 Genomes phase 3) ===\n")
h = f"{'cat':11}{'gene':11}{'al':3}" + "".join(f"{c[0][:12]:>13}" for c in COLS)
print(h); print("-"*len(h))
for r in rows:
    print(f"{r['category']:11}{r['gene']:11}{r['allele']:3}" +
          "".join((f"{r[c[0]]*100:11.1f}%" if r[c[0]] is not None else f"{'n/a':>12} ") for c in COLS))
print("\nSaved: allele_frequencies.csv, raw_variation.json")

#!/usr/bin/env python3
"""
Antarctic meteorite analysis.

Data: The Meteoritical Society "Meteorite Landings" catalogue (45,716 records),
      via NASA Open Data / figshare mirror (data/meteorites_world.csv).
      Fields: name, id, nametype, recclass, mass (g), fall, year, reclat, reclong.
      NOTE: this snapshot effectively ends ~2013, so per-decade counts after
      2000 are truncated by the catalogue, not by fewer discoveries.

Run:  python3 analyze_meteorites.py   (needs pandas)
"""
import pandas as pd, re

df = pd.read_csv("data/meteorites_world.csv")
df.columns = ["name", "id", "nametype", "recclass", "mass", "fall",
              "year", "lat", "lon", "geo"]
df["year"] = pd.to_numeric(df["year"], errors="coerce")

# Antarctic = far-south coordinates OR a known Antarctic collection-field name
# whose coordinates are not clearly northern. Short abbreviation codes (ALH, QUE,
# ...) are anchored to the start of the name so they don't match substrings like
# "Ka(mil)" or "(San) Juan" — a loose contains() otherwise leaks ~280 non-Antarctic
# meteorites (e.g. Gebel Kamil in Egypt) into the set.
FIELD_WORDS = ("Allan Hills", "Queen Alexandra", "Elephant Moraine", "Lewis Cliff",
               "Grove Mountains", "Grosvenor", "Miller Range", "MacAlpine", "Pecora",
               "Graves Nunatak", "Reckling", "Meteorite Hills", "Frontier Mountain",
               "Larkman", "LaPaz", "Dominion Range", "Scott Glacier", "Cumulus Hills",
               "Wisconsin Range")
SHORT = r"^(ALHA?|LEW|QUE|EETA?|MIL|GRO|PCA|GRA|RKP|TIL|MET|MAC|LAR|BTN|FRO|DOM|Yamato|Asuka)\b"
namehit = (df["name"].str.contains("|".join(FIELD_WORDS), case=False, na=False)
           | df["name"].str.match(SHORT, case=False))
not_north = df["lat"].isna() | (df["lat"] < -40) | ((df["lat"] == 0) & (df["lon"] == 0))
df["antarctic"] = (df["lat"] < -60) | (namehit & not_north)
ant = df[df.antarctic]
rest = df[~df.antarctic]


def pct(n, d):
    return f"{100*n/d:.0f}%"


print("=" * 60)
print("1. CONCENTRATION")
print("=" * 60)
print(f"All known meteorites : {len(df):,}")
print(f"From Antarctica      : {len(ant):,}  ({pct(len(ant), len(df))} of every meteorite on Earth)")
print(f"Rest of the world    : {len(rest):,}")

print("\n" + "=" * 60)
print("2. NOBODY EVER SEES THEM FALL")
print("=" * 60)
print("Antarctic  fell/found:", ant.fall.value_counts().to_dict())
print("Elsewhere  fell/found:", rest.fall.value_counts().to_dict())

print("\n" + "=" * 60)
print("3. THEY ARE TINY  (systematic pickup finds even pebbles)")
print("=" * 60)
print(f"Antarctic median mass: {ant['mass'].median():.0f} g")
print(f"Elsewhere median mass: {rest['mass'].median():.0f} g")

print("\n" + "=" * 60)
print("4. ROCKS FROM MARS AND THE MOON")
print("=" * 60)
for label, key in [("Martian", "Martian"), ("Lunar", "Lunar")]:
    sub = df[df.recclass.str.contains(key, case=False, na=False)]
    a = sub[sub.antarctic]
    print(f"{label}: {len(sub)} catalogued, {len(a)} Antarctic. e.g. {list(a.name.head(3))}")

print("\n" + "=" * 60)
print("5. WHAT KIND OF ROCKS THEY ARE")
print("=" * 60)
def kind(c):
    c = str(c).strip()
    if "Martian" in c: return "From Mars"
    if "Lunar" in c: return "From the Moon"
    if re.match(r"H[0-9~/]", c) or c == "H": return "Ordinary chondrite H"
    if c.startswith("LL"): return "Ordinary chondrite LL"
    if re.match(r"L[0-9~/]", c) or c == "L": return "Ordinary chondrite L"
    if c.startswith("C"): return "Carbonaceous chondrite"
    if re.match(r"E[0-9]", c): return "Enstatite chondrite"
    if re.search(r"\bIron\b", c): return "Iron"
    if "Pallasite" in c or "Mesosiderite" in c: return "Stony-iron"
    if any(k in c for k in ("Eucrite", "Diogenite", "Howardite", "Ureilite", "Aubrite",
                            "Angrite", "Lodranite", "Acapulco")): return "Achondrite (asteroidal)"
    return "Other / unclassified"
vc = ant.recclass.apply(kind).value_counts()
for k, v in vc.items():
    print(f"  {k:26s} {v:6,d}  {100*v/len(ant):4.1f}%")

print("\n" + "=" * 60)
print("6. THE IRON PARADOX  (irons are missing from the ice)")
print("=" * 60)
iron = r"\bIron\b|Pallasite|Mesosiderite"
a_iron = ant.recclass.str.contains(iron, na=False).mean()
falls = df[df.fall == "Fell"]
f_iron = falls.recclass.str.contains(iron, na=False).mean()
print(f"Iron / stony-iron share in Antarctica : {100*a_iron:.2f}%")
print(f"Iron / stony-iron among world 'Fell'  : {100*f_iron:.2f}%")
print(f"=> irons are ~{f_iron/a_iron:.0f}x under-represented in the ice "
      f"(they warm in sunlight and sink below the surface).")

print("\n" + "=" * 60)
print("7. TOP BLUE-ICE STRANDING FIELDS")
print("=" * 60)
def field(n):
    for w in FIELD_WORDS:
        if re.search(w, str(n), re.I):
            return w
    m = re.match(SHORT, str(n), re.I)
    if m:
        return {"ALH": "Allan Hills", "LEW": "Lewis Cliff", "QUE": "Queen Alexandra",
                "EET": "Elephant Moraine", "MIL": "Miller Range",
                "GRO": "Grove Mountains"}.get(m.group(1).upper(), m.group(1))
    return "other"
vc = ant["name"].apply(field).value_counts().head(10)
for f, c in vc.items():
    print(f"  {f:20s} {c:6,d}")

print("\n" + "=" * 60)
print("8. DISCOVERY TIMELINE  (Antarctic finds/decade; catalogue ends ~2013)")
print("=" * 60)
t = ant[(ant.year >= 1960) & (ant.year <= 2013)]
print((t.year // 10 * 10).value_counts().sort_index().to_string())

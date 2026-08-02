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

# Antarctic = far-south coordinates OR a known Antarctic collection-field name.
FIELDS = ("Yamato", "Asuka", "Allan Hills", "Queen Alexandra", "Elephant Moraine",
          "Lewis Cliff", "Grove Mountains", "Grosvenor", "Miller Range", "MacAlpine",
          "Pecora", "Graves Nunatak", "Reckling", "Meteorite Hills", "Frontier Mountain",
          "Larkman", "LaPaz", "Dominion Range", "Scott Glacier", "Cumulus Hills",
          "Wisconsin Range", "ALH", "LEW", "QUE", "EET", "MIL", "GRO")
namehit = df["name"].str.contains("|".join(FIELDS), case=False, na=False)
df["antarctic"] = (df["lat"] < -60) | namehit
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
print("5. TOP BLUE-ICE STRANDING FIELDS")
print("=" * 60)
def field(n):
    for f in FIELDS:
        if re.search(f, str(n), re.I):
            return {"ALH": "Allan Hills", "LEW": "Lewis Cliff", "QUE": "Queen Alexandra",
                    "EET": "Elephant Moraine", "MIL": "Miller Range",
                    "GRO": "Grove Mountains"}.get(f, f)
    return "other"
vc = ant["name"].apply(field).value_counts().head(10)
for f, c in vc.items():
    print(f"  {f:20s} {c:6,d}")

print("\n" + "=" * 60)
print("6. DISCOVERY TIMELINE  (Antarctic finds/decade; catalogue ends ~2013)")
print("=" * 60)
t = ant[(ant.year >= 1960) & (ant.year <= 2013)]
print((t.year // 10 * 10).value_counts().sort_index().to_string())

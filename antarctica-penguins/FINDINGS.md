# Antarctica, told through penguins — what the data says and the surprising anomalies

**Dataset:** Antarctic Penguin Biogeography Project (MAPPPD) — Che-Castaldo et al.,
*Biodiversity Data Journal* (2024), [doi:10.3897/BDJ.11.e101476](https://doi.org/10.3897/BDJ.11.e101476).
Every published breeding-colony count for the six penguin species south of 60°S.
Source data (CC-BY 4.0): <https://github.com/CCheCastaldo/mapppdr>.

- **5,483** colony counts · **729** sites · **6** species · **1892 → 2022**
- Metric used here: **nest counts** (= breeding pairs), the standard abundance unit.
- Method: for every colony with a ≥15-year record and ≥50 nests, compare the
  mean of its **earliest third** of surveys to its **latest third**. Reproducible
  via [`analyze.py`](./analyze.py).

Why penguins are a good lens on the continent: they are counted from the ground,
from planes, from drones, and increasingly **from satellites that spot the brown
guano stain on the ice** — so a "penguin dataset" is really a long-baseline
record of where the Southern Ocean is still cold enough to raise chicks.

---

## What we know

**1. The Antarctic Peninsula is where the action is.** Nearly every dramatic
change sits on the warming Peninsula and the South Shetland/Orkney islands. The
cold continental interior is comparatively stable.

**2. Penguins are not moving together — they are sorting by temperature.** The
three *Pygoscelis* species that share the same rocks are heading in opposite
directions:

| Species | Colonies analysed | Increasing | Decreasing | Median change |
|---|---:|---:|---:|---:|
| **Gentoo** (temperate-tolerant) | 50 | **76 %** | 24 % | **+63 %** |
| **Adélie** (sea-ice specialist) | 82 | 57 % | 43 % | +8 % |
| **Chinstrap** (open-water, krill-dependent) | 55 | 24 % | **76 %** | **−46 %** |

The pattern is exactly what you'd expect if the Peninsula is warming and losing
sea ice: the ice-and-cold species lose, the warm-water generalist wins.

---

## The surprising anomalies

### 🔻 1. The chinstrap collapse — the "safe" species is crashing
Chinstraps were long considered abundant and secure. In the data, **76 % of
well-monitored colonies are shrinking**, with a median loss of **−46 %**. The
extremes are brutal:

- **Harmony Point:** ~**50,000 → ~1,000 nests** (−98%)
- **Point Thomas (Rakusa Point):** 584 → 2 nests (effectively extirpated)
- **Gourlay Point:** 13,089 → 1,510 nests (−88%)

This is the single most counterintuitive result: the penguin most people would
not worry about is the one falling fastest.

### 🔀 2. A species swap on a single rock
At **8 shared colonies**, chinstraps collapse **and** gentoos boom **on the very
same site** — one species is replacing the other in real time as conditions warm:

| Colony | Chinstrap | Gentoo |
|---|---:|---:|
| Sterneck Island | −96 % | +350 % |
| Ardley Island | −86 % | +103 % |
| Llano Point | −97 % | +76 % |
| Stranger Point | −61 % | +70 % |

You can watch the Southern Ocean's climate zone move by looking at which penguin
owns the guano patch.

### ➡️ 3. Gentoos are marching south
Gentoos aren't just growing — they're **colonising new, higher-latitude ground**.
The number of active gentoo colonies rose **51 → 63 → 91** across 1980–1995 /
1996–2010 / 2011–2023, and the **southernmost** occupied colony crept from
Petermann Island (65.18°S) to Green Island (65.32°S). The most explosive boom:
**Biscoe Point, 54 → 2,405 nests (+4,368%)**.

### ⚖️ 4. The Adélie climate divide — one species, opposite fates
The most elegant anomaly. Split Adélie colonies by latitude and the **same
species does opposite things**:

- **North of 66°S** (warm Peninsula): median **−40 %**, 70 % of colonies declining.
- **South of 70°S** (cold continental coast): median **+30 %**, 79 % increasing.

Averaged across the continent Adélies look "roughly stable" (+8%) — a flat number
that **hides two strong, opposing trends**. The average is the anomaly's disguise.

### 🛰️ 5. Hidden oddities in the data itself
- The largest single count in the database is **Cape Adare: 504,332 Adélie nests**
  (2018, aerial) — one of the biggest seabird colonies on Earth.
- **341 counts are satellite-derived** (very-high-res / Sentinel / Landsat) —
  colonies found and sized from orbit, many never visited on foot.
- Records run from **1892** to future-dated **2026** rows (planned/projected
  surveys); the analysis clips to ≤2023 so projections don't skew trends.

---

## Bottom line
The clean headline "penguin populations are changing" is the least interesting
thing here. The real story is **divergence**: neighbouring species on the same
islands, and even one species along a latitude gradient, are moving in **opposite
directions** — a fingerprint of a warming, sea-ice-losing Antarctic Peninsula
that a single continent-wide average would completely erase.

*Reproduce:* `cd antarctica-penguins && python3 analyze.py` (needs `pandas`).

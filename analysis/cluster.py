#!/usr/bin/env python3
"""Cluster populations by overall similarity across the allele-frequency panel.
Pure Python (no numpy): Euclidean distance + average-linkage hierarchical
clustering, rendered as a dendrogram SVG. Also writes a distance matrix CSV."""
import csv, math

rows = list(csv.DictReader(open("allele_frequencies.csv")))
POPS = ["KHV (Viet~Fil)","CDX (Dai~Fil)","CHB (Han)","JPT (Japan)","EAS",
        "SAS","EUR","AFR","YRI (Nigeria)","PEL (Peru)"]

# Build a frequency vector per population (skip cells that are n/a in any SNP).
vecs = {p: [] for p in POPS}
usable = 0
for r in rows:
    vals = {p: r[p] for p in POPS}
    if any(vals[p] in ("", None) for p in POPS):
        continue
    usable += 1
    for p in POPS:
        vecs[p].append(float(vals[p]))
print(f"Using {usable}/{len(rows)} SNPs (complete across all populations)")

def dist(a, b):
    return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))

# distance matrix
D = {(i, j): dist(vecs[POPS[i]], vecs[POPS[j]]) for i in range(len(POPS)) for j in range(len(POPS))}
with open("population_distance_matrix.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow([""] + POPS)
    for i, p in enumerate(POPS):
        w.writerow([p] + [round(D[(i, j)], 3) for j in range(len(POPS))])

# average-linkage agglomerative clustering
clusters = [{"members": [i], "id": POPS[i], "h": 0.0, "x": None} for i in range(len(POPS))]
def cdist(A, B):
    return sum(dist(vecs[POPS[i]], vecs[POPS[j]]) for i in A["members"] for j in B["members"]) / (len(A["members"])*len(B["members"]))

merges = []
while len(clusters) > 1:
    best = None
    for i in range(len(clusters)):
        for j in range(i+1, len(clusters)):
            d = cdist(clusters[i], clusters[j])
            if best is None or d < best[0]:
                best = (d, i, j)
    d, i, j = best
    A, B = clusters[i], clusters[j]
    merged = {"members": A["members"]+B["members"], "id": f"({A['id']},{B['id']})",
              "h": d, "left": A, "right": B}
    merges.append((A["id"], B["id"], round(d, 2)))
    clusters = [c for k, c in enumerate(clusters) if k not in (i, j)] + [merged]
root = clusters[0]

print("\nMerge order (closest first):")
for a, b, d in merges:
    print(f"  d={d:6.2f}  {a}  +  {b}")

# ---- render dendrogram SVG ----
leaf_order = []
def collect(n):
    if "left" not in n: leaf_order.append(n["members"][0]); return
    collect(n["left"]); collect(n["right"])
collect(root)

Wd, LEAF_GAP, TOP, LEFT = 760, 46, 60, 150
maxh = root["h"] or 1
xscale = (Wd - LEFT - 170) / maxh
ypos = {m: TOP + k*LEAF_GAP for k, m in enumerate(leaf_order)}
H = TOP + len(leaf_order)*LEAF_GAP + 40
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{H}" font-family="system-ui,Arial,sans-serif">',
       f'<rect width="{Wd}" height="{H}" fill="white"/>',
       f'<text x="20" y="34" font-size="19" font-weight="700" fill="#12303a">Populations clustered by overall similarity</text>',
       f'<text x="20" y="52" font-size="12" fill="#5a6b72">Average-linkage on {usable} SNPs (Ensembl / 1000 Genomes). Shorter joins = more genetically alike.</text>']
def x_at(h): return LEFT + (maxh - h)*xscale
def draw(n):
    if "left" not in n:
        m = n["members"][0]; y = ypos[m]
        hl = "#0a5160" if POPS[m].startswith(("KHV","CDX")) else "#12303a"
        svg.append(f'<text x="{Wd-160}" y="{y+4}" font-size="12.5" fill="{hl}" font-weight="{700 if hl!="#12303a" else 400}">{POPS[m]}</text>')
        return y, x_at(0)
    yl, xl = draw(n["left"]); yr, xr = draw(n["right"])
    xj = x_at(n["h"])
    for (yy, xx) in ((yl, xl), (yr, xr)):
        svg.append(f'<line x1="{xj}" y1="{yy}" x2="{xx}" y2="{yy}" stroke="#3a6b78" stroke-width="1.6"/>')
    svg.append(f'<line x1="{xj}" y1="{yl}" x2="{xj}" y2="{yr}" stroke="#3a6b78" stroke-width="1.6"/>')
    return (yl+yr)/2, xj
draw(root)
svg.append(f'<text x="20" y="{H-14}" font-size="10.5" fill="#9aa7ac">KHV/CDX = nearest proxies to Filipino ancestry (teal) &#183; momentum-font world-history research</text>')
svg.append("</svg>")
open("population_dendrogram.svg", "w").write("\n".join(svg))
print("\nLeaf order:", " > ".join(POPS[m] for m in leaf_order))
print("Wrote: population_distance_matrix.csv, population_dendrogram.svg")

#!/usr/bin/env python3
"""Render allele_frequencies.csv (categorized panel) as a self-contained SVG heatmap."""
import csv

rows = list(csv.DictReader(open("allele_frequencies.csv")))
POPS = ["KHV (Viet~Fil)","CDX (Dai~Fil)","CHB (Han)","JPT (Japan)","EAS",
        "SAS","EUR","AFR","YRI (Nigeria)","PEL (Peru)"]
CATCOL = {"Diet":"#c9772a","Pigment":"#7a5bb0","Morphology":"#2a8ca8",
          "Disease":"#c0453f","Physical":"#3f8f5a"}

GUT = 30                 # category gutter (rotated labels)
LEFTW = 268              # gene/trait text
LEFT = GUT + LEFTW
CW, CH = 74, 42
TOP = 116
W = LEFT + CW*len(POPS) + 18
H = TOP + CH*len(rows) + 92

def lerp(a,b,t): return a+(b-a)*t
def color(f):
    c0=(238,246,248); c1=(10,81,96)
    return "rgb(%d,%d,%d)"%tuple(int(lerp(c0[i],c1[i],f)) for i in range(3))

s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="system-ui,Arial,sans-serif">']
s.append(f'<rect width="{W}" height="{H}" fill="white"/>')
s.append(f'<text x="18" y="32" font-size="22" font-weight="700" fill="#12303a">Human trait &amp; ancestry allele frequencies</text>')
s.append(f'<text x="18" y="56" font-size="13" fill="#5a6b72">Real data: Ensembl REST API / 1000 Genomes phase 3 &#183; {len(rows)} SNPs &#215; {len(POPS)} populations &#183; % carrying the highlighted allele</text>')
s.append(f'<text x="18" y="76" font-size="12" fill="#8a4b0a">No Filipino sample exists in 1000 Genomes &#8212; KHV (Vietnamese) &amp; CDX (Dai) are the nearest proxies (two leftmost columns).</text>')

# column headers
for j,p in enumerate(POPS):
    x=LEFT+j*CW+CW/2
    parts=p.split(" (")
    code=parts[0]; sub="("+parts[1] if len(parts)>1 else ""
    hl = "#0a5160" if p.startswith(("KHV","CDX")) else "#12303a"
    s.append(f'<text x="{x}" y="{TOP-32}" font-size="12" font-weight="700" text-anchor="middle" fill="{hl}">{code}</text>')
    if sub:
        s.append(f'<text x="{x}" y="{TOP-17}" font-size="9.5" text-anchor="middle" fill="#6b7b82">{sub}</text>')

# category groups + separators
i=0
while i < len(rows):
    cat=rows[i]["category"]
    j=i
    while j < len(rows) and rows[j]["category"]==cat: j+=1
    y0=TOP+i*CH; y1=TOP+j*CH
    col=CATCOL.get(cat,"#888")
    s.append(f'<rect x="{GUT-8}" y="{y0+2}" width="5" height="{y1-y0-4}" rx="2" fill="{col}"/>')
    cy=(y0+y1)/2
    s.append(f'<text x="16" y="{cy}" font-size="12" font-weight="700" fill="{col}" text-anchor="middle" transform="rotate(-90 16 {cy})">{cat}</text>')
    if i>0:
        s.append(f'<line x1="{GUT}" y1="{y0}" x2="{W-10}" y2="{y0}" stroke="#e3eaec" stroke-width="1.5"/>')
    i=j

# rows
for i,r in enumerate(rows):
    y=TOP+i*CH
    s.append(f'<text x="{GUT+4}" y="{y+CH/2-2}" font-size="13" font-weight="700" fill="#12303a">{r["gene"]}</text>')
    s.append(f'<text x="{GUT+4}" y="{y+CH/2+14}" font-size="10" fill="#6b7b82">{r["trait"]}</text>')
    s.append(f'<text x="{LEFT-10}" y="{y+CH/2+5}" font-size="11" text-anchor="end" fill="#0a5160" font-weight="700">{r["highlight_allele"]}</text>')
    for jx,p in enumerate(POPS):
        x=LEFT+jx*CW; v=r[p]
        if v=="" or v is None:
            s.append(f'<rect x="{x+2}" y="{y+2}" width="{CW-4}" height="{CH-4}" rx="4" fill="#f2f2f2"/>')
            s.append(f'<text x="{x+CW/2}" y="{y+CH/2+4}" font-size="10" text-anchor="middle" fill="#aaa">n/a</text>')
            continue
        f=float(v)
        s.append(f'<rect x="{x+2}" y="{y+2}" width="{CW-4}" height="{CH-4}" rx="4" fill="{color(f)}"/>')
        txt="#ffffff" if f>0.5 else "#12303a"
        s.append(f'<text x="{x+CW/2}" y="{y+CH/2+5}" font-size="12" font-weight="600" text-anchor="middle" fill="{txt}">{f*100:.0f}%</text>')

# legend
ly=TOP+len(rows)*CH+38
s.append(f'<text x="18" y="{ly+4}" font-size="11.5" fill="#5a6b72">Allele frequency:</text>')
for k in range(11):
    s.append(f'<rect x="{130+k*26}" y="{ly-10}" width="26" height="16" fill="{color(k/10)}"/>')
s.append(f'<text x="130" y="{ly+22}" font-size="10.5" fill="#6b7b82">0%</text>')
s.append(f'<text x="{130+11*26-18}" y="{ly+22}" font-size="10.5" fill="#6b7b82">100%</text>')
s.append(f'<text x="18" y="{H-14}" font-size="10.5" fill="#9aa7ac">Generated from Ensembl REST API &#183; momentum-font world-history research &#183; frequencies are population-level, not individual predictions</text>')
s.append("</svg>")
open("allele_frequencies.svg","w").write("\n".join(s))
print("wrote allele_frequencies.svg", W, "x", H)

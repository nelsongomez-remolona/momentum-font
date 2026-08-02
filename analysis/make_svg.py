#!/usr/bin/env python3
"""Render allele_frequencies.csv as a self-contained SVG heatmap."""
import csv

rows = list(csv.DictReader(open("allele_frequencies.csv")))
POPS = ["KHV (Vietnamese)","CDX (Dai)","CHB (Han)","JPT (Japanese)","EAS (E Asian)",
        "SAS (S Asian)","EUR (European)","AFR (African)","PEL (Peruvian)"]

CW, CH = 80, 48          # cell size
LEFT, TOP = 300, 108     # margins
W = LEFT + CW*len(POPS) + 20
H = TOP + CH*len(rows) + 92

def lerp(a,b,t): return a+(b-a)*t
def color(f):
    # light (#eef6f8) -> deep teal (#0a5160)
    c0=(238,246,248); c1=(10,81,96)
    r,g,b=[int(lerp(c0[i],c1[i],f)) for i in range(3)]
    return f"rgb({r},{g},{b})"

s=[]
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="system-ui,Arial,sans-serif">')
s.append(f'<rect width="{W}" height="{H}" fill="white"/>')
s.append(f'<text x="20" y="34" font-size="21" font-weight="700" fill="#12303a">Trait &amp; ancestry allele frequencies</text>')
s.append(f'<text x="20" y="58" font-size="13" fill="#5a6b72">Real data: Ensembl REST API / 1000 Genomes phase 3 &#183; % carrying the highlighted allele</text>')
s.append(f'<text x="20" y="80" font-size="12" fill="#8a4b0a">No Filipino sample exists in 1000 Genomes &#8212; KHV (Vietnamese) &amp; CDX (Dai) are the nearest proxies (leftmost).</text>')

# column headers
for j,p in enumerate(POPS):
    x=LEFT+j*CW+CW/2
    parts=p.split(" (")
    code=parts[0]; sub="("+parts[1] if len(parts)>1 else ""
    hl = "#0a5160" if p.startswith(("KHV","CDX")) else "#12303a"
    s.append(f'<text x="{x}" y="{TOP-30}" font-size="12.5" font-weight="700" text-anchor="middle" fill="{hl}">{code}</text>')
    s.append(f'<text x="{x}" y="{TOP-14}" font-size="10.5" text-anchor="middle" fill="#6b7b82">{sub}</text>')

# rows
for i,r in enumerate(rows):
    y=TOP+i*CH
    gene=r["gene"]; trait=r["trait"]; allele=r["highlight_allele"]
    s.append(f'<text x="20" y="{y+CH/2-2}" font-size="13.5" font-weight="700" fill="#12303a">{gene}</text>')
    s.append(f'<text x="20" y="{y+CH/2+15}" font-size="10.5" fill="#6b7b82">{trait}</text>')
    s.append(f'<text x="{LEFT-14}" y="{y+CH/2+5}" font-size="11" text-anchor="end" fill="#0a5160" font-weight="700">{allele}</text>')
    for j,p in enumerate(POPS):
        x=LEFT+j*CW
        v=r[p]
        if v=="" or v is None:
            s.append(f'<rect x="{x+2}" y="{y+2}" width="{CW-4}" height="{CH-4}" rx="4" fill="#f2f2f2"/>')
            s.append(f'<text x="{x+CW/2}" y="{y+CH/2+4}" font-size="11" text-anchor="middle" fill="#aaa">n/a</text>')
            continue
        f=float(v)
        s.append(f'<rect x="{x+2}" y="{y+2}" width="{CW-4}" height="{CH-4}" rx="4" fill="{color(f)}"/>')
        txt="#ffffff" if f>0.5 else "#12303a"
        s.append(f'<text x="{x+CW/2}" y="{y+CH/2+5}" font-size="12.5" font-weight="600" text-anchor="middle" fill="{txt}">{f*100:.0f}%</text>')

# legend
ly=TOP+len(rows)*CH+34
s.append(f'<text x="20" y="{ly+4}" font-size="11.5" fill="#5a6b72">Allele frequency:</text>')
for k in range(0,11):
    f=k/10; x=140+k*26
    s.append(f'<rect x="{x}" y="{ly-10}" width="26" height="16" fill="{color(f)}"/>')
s.append(f'<text x="140" y="{ly+22}" font-size="10.5" fill="#6b7b82">0%</text>')
s.append(f'<text x="{140+11*26-18}" y="{ly+22}" font-size="10.5" fill="#6b7b82">100%</text>')
s.append(f'<text x="20" y="{H-14}" font-size="10.5" fill="#9aa7ac">Generated from Ensembl REST API, {len(rows)} SNPs · momentum-font world-history research</text>')
s.append("</svg>")
open("allele_frequencies.svg","w").write("\n".join(s))
print("wrote allele_frequencies.svg", W, "x", H)

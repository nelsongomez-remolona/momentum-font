#!/usr/bin/env python3
"""
Antarctic climate anomaly analysis from two open datasets.

  1. NSIDC Sea Ice Index v4.0 (monthly extent, Southern Hemisphere, 1979- )
     https://nsidc.org/data/g02135  (data/seaice/S_MM.csv)
  2. SCAR READER surface air temperature (station monthly means)
     https://legacy.bas.ac.uk/met/READER/  (data/reader/<station>.temperature.txt)

Run:  python3 analyze_climate.py   (needs numpy)
"""
import numpy as np, os, glob

SI = "data/seaice/"
RE = "data/reader/"

# ----------------------------------------------------------------- sea ice
def sea_ice():
    def month(m):
        yrs, ext = [], []
        for line in open(f"{SI}S_{m:02d}.csv"):
            p = [x.strip() for x in line.split(",")]
            if len(p) < 6 or not p[0].isdigit():
                continue
            try:
                e = float(p[4])
            except ValueError:
                continue
            if e > 0:
                yrs.append(int(p[0])); ext.append(e)
        return dict(zip(yrs, ext))
    feb, sep = month(2), month(9)
    print("=" * 68)
    print("SEA ICE INDEX  (million km^2, NSIDC v4.0)")
    print("=" * 68)
    for label, s in [("Summer minimum (Feb)", feb), ("Winter maximum (Sep)", sep)]:
        clim = np.mean([s[y] for y in range(1981, 2011) if y in s])
        lo_y = min(s, key=s.get)
        print(f"\n{label}:  1981-2010 normal = {clim:.2f}")
        print(f"  record low   {s[lo_y]:.2f}  in {lo_y}   ({100*(s[lo_y]-clim)/clim:+.0f}% vs normal)")
        pre = np.mean([s[y] for y in s if 1979 <= y <= 2015])
        post = np.mean([s[y] for y in s if 2016 <= y <= 2025])
        print(f"  1979-2015 mean {pre:.2f}   ->   2016-2025 mean {post:.2f}   ({post-pre:+.2f})")
    # lowest complete calendar years by annual mean (exclude partial current year)
    allm = {}
    for m in range(1, 13):
        for y, e in month(m).items():
            allm.setdefault(y, []).append(e)
    ann = {y: np.mean(v) for y, v in allm.items() if len(v) == 12}
    order = sorted(ann, key=ann.get)[:5]
    print("\n5 lowest COMPLETE years by annual-mean extent:")
    for y in order:
        print(f"  {y}: {ann[y]:.2f}")


# -------------------------------------------------------------- temperature
META = {  # station: (region bucket, latitude)
 'Faraday': ('Peninsula', -65.2), 'Rothera': ('Peninsula', -67.6),
 'Esperanza': ('Peninsula', -63.4), 'Bellingshausen': ('Peninsula', -62.2),
 'Marambio': ('Peninsula', -64.2), 'Orcadas': ('Peninsula', -60.7),
 'Halley': ('Coast', -75.6), 'Neumayer': ('Coast', -70.7),
 'Casey': ('Coast', -66.3), 'Mawson': ('Coast', -67.6), 'Davis': ('Coast', -68.6),
 'Novolazarevskaya': ('Coast', -70.8), 'Syowa': ('Coast', -69.0),
 'Scott_Base': ('Coast', -77.8), 'McMurdo': ('Coast', -77.9),
 'Vostok': ('Interior', -78.5), 'Amundsen_Scott': ('Interior', -90.0),
}

def annual(fn):
    yrs, temps = [], []
    for line in open(fn):
        p = line.split()
        if len(p) >= 13 and p[0].isdigit():
            vals = []
            for x in p[1:13]:
                try:
                    v = float(x)
                    if v > -99: vals.append(v)
                except ValueError:
                    pass
            if len(vals) >= 10:
                yrs.append(int(p[0])); temps.append(np.mean(vals))
    return np.array(yrs, float), np.array(temps, float)

def temperature():
    print("\n" + "=" * 68)
    print("SURFACE TEMPERATURE TREND  (deg C per decade, SCAR READER)")
    print("=" * 68)
    rows = []
    for s, (reg, lat) in META.items():
        fn = f"{RE}{s}.temperature.txt"
        if not os.path.exists(fn): continue
        yr, t = annual(fn)
        if len(yr) < 20: continue          # require a real long record
        slope = np.polyfit(yr, t, 1)[0] * 10
        rows.append((s, reg, lat, int(yr.min()), int(yr.max()), t.mean(), slope))
    rows.sort(key=lambda r: -r[6])
    print(f"{'Station':17s}{'Region':10s}{'span':>12s}{'mean':>8s}{'/decade':>10s}")
    for s, reg, lat, y0, y1, m, b in rows:
        print(f"{s:17s}{reg:10s}{f'{y0}-{y1}':>12s}{m:8.1f}{b:+10.2f}")
    for reg in ("Peninsula", "Coast", "Interior"):
        v = [r[6] for r in rows if r[1] == reg]
        print(f"  mean {reg:10s} {np.mean(v):+.2f} deg C/decade  (n={len(v)})")


if __name__ == "__main__":
    sea_ice()
    temperature()

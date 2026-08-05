"""
End-to-end: fetch DEM over an Amazon region, detect candidate structures,
render products, and print a ranked report.

Default region: the ACRE GEOGLYPHS belt in western Brazil (near Rio Branco),
where hundreds of pre-Columbian ditched enclosures were found under forest.
These are large (100-300 m) -- the only class of Amazonian earthwork that
30 m open elevation data has any chance of hinting at.

Usage:
    python run.py                      # default Acre region
    python run.py --preset mojos       # Llanos de Mojos, Bolivia
    python run.py --west -67.6 --south -10.05 --east -67.35 --north -9.85
    python run.py --geotiff bare_earth.tif   # your own real LiDAR DEM
"""

from __future__ import annotations

import argparse
import os

from dem_fetch import BBox, fetch_dem, save_dem, load_geotiff
from detect import detect, save_candidates
from visualize import render_all

PRESETS = {
    # west, south, east, north
    "acre":  BBox(-67.62, -10.05, -67.35, -9.82),   # Acre geoglyph belt, Brazil
    "mojos": BBox(-65.10, -14.60, -64.85, -14.38),  # Llanos de Mojos, Bolivia
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", choices=PRESETS.keys(), default="acre")
    ap.add_argument("--west", type=float)
    ap.add_argument("--south", type=float)
    ap.add_argument("--east", type=float)
    ap.add_argument("--north", type=float)
    ap.add_argument("--zoom", type=int, default=12)
    ap.add_argument("--geotiff", type=str, default=None,
                    help="use a real bare-earth LiDAR DEM instead of fetching")
    ap.add_argument("--out", type=str, default="output")
    ap.add_argument("--cache", type=str, default="tile_cache")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    if args.geotiff:
        print(f"[run] loading real DEM from {args.geotiff}")
        dem = load_geotiff(args.geotiff)
    else:
        if args.west is not None:
            bbox = BBox(args.west, args.south, args.east, args.north)
        else:
            bbox = PRESETS[args.preset]
        print(f"[run] region: {bbox}")
        dem = fetch_dem(bbox, zoom=args.zoom, cache_dir=args.cache)

    print(f"[run] DEM {dem.elev.shape}, ~{dem.meters_per_px:.1f} m/px, "
          f"elev {dem.elev.min():.0f}-{dem.elev.max():.0f} m")
    save_dem(dem, os.path.join(args.out, "dem"))

    cands = detect(dem)
    save_candidates(cands, os.path.join(args.out, "candidates.geojson"))
    paths = render_all(dem, cands, args.out)

    print(f"\n[run] rendered: {', '.join(paths.values())}")
    print(f"[run] {len(cands)} candidate structures (top 15):\n")
    print(f"  {'rank':>4}  {'kind':<6} {'lat':>10} {'lon':>10} "
          f"{'diam_m':>7} {'amp_m':>6} {'reg':>5} {'score':>6}")
    for i, c in enumerate(cands[:15], 1):
        print(f"  {i:>4}  {c.kind:<6} {c.lat:>10.5f} {c.lon:>10.5f} "
              f"{c.diameter_m:>7.0f} {c.amplitude_m:>6.2f} "
              f"{c.regularity:>5.2f} {c.score:>6.2f}")
    print("\n[run] NOTE: candidates are *screening hits*, not confirmed sites. "
          "At 30 m resolution most real geoglyphs are near the detection limit; "
          "verify each against high-res imagery / bare-earth LiDAR.")


if __name__ == "__main__":
    main()

# Amazon LiDAR structure-detection pipeline

A small, honest, end-to-end pipeline that **pulls elevation ("LiDAR-style")
data over the Amazon and screens it for candidate pre-Columbian earthworks** —
mounds, platforms, and ditched enclosures ("geoglyphs").

It runs today, against real public data, with no API key.

```bash
pip install -r requirements.txt
python run.py                 # default: Acre geoglyph belt, Brazil
python run.py --preset mojos  # Llanos de Mojos, Bolivia
python test_pipeline.py       # offline tests (no network)
```

Outputs land in `output/`: `hillshade.png`, `lrm.png`, `candidates.png`,
`dem.npy`/`dem.json`, and `candidates.geojson` (openable in QGIS / geojson.io).

## Read this first — what this is and isn't

**The honest version:** I cannot commission an aircraft to fly LiDAR over the
rainforest, and no one has handed us an undiscovered lost city. What this does
is the *real method* archaeologists use, wired to the best **open, key-free**
elevation data available:

- **Data source:** AWS [Terrain Tiles](https://registry.opendata.aws/terrain-tiles/)
  (Terrarium PNG encoding) — a global mosaic derived from **SRTM (~30 m)** and
  friends. It is a **surface** model (canopy included), **not** the
  canopy-removed, sub-meter **bare-earth LiDAR** that real discoveries use
  (e.g. Prümers et al. 2022, *Nature*, on the Casarabe sites).
- **What 30 m can and can't see:** it cannot resolve a 1–2 m mound. It can only
  *hint* at the very largest earthworks (100–300 m enclosures and causeways).
  So treat every hit as a **screening candidate**, not a discovery. Look at the
  `lrm.png` for the Acre run and you'll see the dominant signal is natural
  river dissection — exactly the honest result.
- **The upgrade path is one flag.** Feed the same pipeline a genuine bare-earth
  LiDAR DEM and it resolves real archaeology:
  ```bash
  python run.py --geotiff your_bare_earth_lidar.tif   # needs rasterio
  ```

## How it works

| Stage | File | What it does |
|-------|------|--------------|
| **Fetch** | `dem_fetch.py` | bbox → slippy tiles → decode Terrarium → stitched, georeferenced DEM |
| **Detect** | `detect.py` | Local Relief Model (DEM − smoothed DEM) isolates small local relief; blobs are extracted, filtered by size + roundness, scored, and geolocated |
| **Visualize** | `visualize.py` | hillshade, diverging LRM map, candidate overlay |
| **Orchestrate** | `run.py` | runs it all, writes GeoJSON, prints a ranked report |

The **Local Relief Model** (Hesse 2010) is the workhorse: subtracting a
low-pass copy of the terrain strips away valleys and regional slope, leaving
the low-amplitude bumps and ditches where earthworks live.

Detection is deliberately **resolution-agnostic** — `feature_scale_m`,
`min_diameter_m`, etc. are in *meters*, so the identical code that screens 30 m
SRTM will find much smaller features in 1 m LiDAR.

## If you want to do this for real

1. Get bare-earth LiDAR: OpenTopography, NASA GEDI-derived products, ANA/INPE
   (Brazil), or a commissioned survey; classify to ground returns.
2. Run `--geotiff` on it.
3. Verify every candidate against high-res optical imagery, existing site
   databases, and — ultimately — ground survey. LiDAR *finds*; it doesn't
   *confirm*.

Coordinates are reported in WGS84 lon/lat so hits drop straight onto a map.

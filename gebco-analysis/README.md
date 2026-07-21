# GEBCO deep-sea field analysis — Cayman Trough to the Puerto Rico Trench

Data products and findings from an exploration of the GEBCO seafloor grid across
the Caribbean's deep frontier (15–22°N, 85–64°W).

## Contents

- `cayman-puerto-rico-map.html` — self-contained interactive field map. GEBCO
  bathymetry basemap with every depth feature plotted and symbolized by data
  provenance (solid = sonar-measured, hollow/dashed = satellite-predicted),
  plus a Cayman Trough close-up with along-axis and cross-trough depth profiles.
  Mobile-optimized; opens in any browser with no dependencies.
- `data/cayman_profiles.json` — along-axis and cross-trough depth profiles of the
  Cayman Trough, with per-point TID provenance.
- `data/analysis_results.json` — machine-readable summary of every result below.

## Sources

- Basemap imagery: GEBCO web map service (`wms.gebco.net`), layer `GEBCO_LATEST`.
- Depth grid: `GEBCO_2020` via NOAA ERDDAP (`coastwatch.pfeg.noaa.gov`).
- Provenance: GEBCO Type Identifier (TID) grid, queried per point via WMS
  `GetFeatureInfo`. TID 10–17 = direct measurement (11 = multibeam); TID 40 =
  predicted from satellite-derived gravity (interpolated, not sounded).
- Earthquake: USGS event `us7000pcdl` (M7.6, 8 Feb 2025).

## Findings

### 1. Provenance is the opposite of intuition

The famous, deep **Puerto Rico Trench is fully sonar-mapped** — 16 of 16 points
along its deepest axis are multibeam (TID 11), including the −8,555 m deepest
cell. That cell is real data reading ~180 m deeper than the cited Brownson Deep
figure (likely an uncleaned outlier), **not** a satellite-interpolation artifact.

The less-visited **Cayman Trough's deepest reaches are largely guesswork** — its
deepest reported cell (−7,323 m) and 32% of its deepest axis are satellite-gravity
*predicted*, never sounded. Because predicted bathymetry under-reads narrow
trenches, the true floor is probably deeper than the grid shows.

### 2. You can catch the interpolation from texture — but only at the right scale

Testing whether satellite-predicted seafloor is detectable from depth texture
alone (130 Cayman ocean samples, validated against TID):

- A **coarse 5 km roughness metric fails**: predicted is only 1.3× smoother than
  measured, and an apparent "75% classifier accuracy" turned out to be a
  base-rate artifact (73% of samples are predicted, so guessing "predicted"
  scores 73% by default).
- A **cell-scale Laplacian metric works**: predicted seafloor is **3.6× smoother**
  at the grid scale (below satellite gravity's ~6 km resolution limit), giving
  **76% balanced accuracy** (76% sensitivity / 75% specificity) at blind
  measured-vs-predicted classification. The interpolation is invisible at coarse
  scale and betrays itself at fine scale — exactly where the physics predicts.

### 3. Coverage tracks survey effort, not depth

Measured fraction by depth band is non-monotonic (0% on shallow slopes, 20% at
1–3 km, 36% at 3–5 km, 27% in the deeps). Coverage follows wherever ships had a
reason to run multibeam (transits, vent-field and ridge surveys), not depth per
se. Overall, ~73% of the sampled Cayman seafloor is predicted, not sounded —
the global "three-quarters unmapped" figure reproduced in a single basin.

## Method note

Provenance was queried live from GEBCO's TID grid; depth statistics and profiles
were computed from the GEBCO_2020 grid. Roughness is a detrended RMS (coarse
metric) and the RMS of the discrete Laplacian over a ~3 km window (cell-scale
metric). Classifier accuracy is reported as balanced accuracy to correct for the
predicted-class base rate. Sample size is modest (n=130, one basin), so the
texture and coverage figures are indicative rather than definitive.

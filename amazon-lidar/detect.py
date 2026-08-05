"""
Detect candidate anthropogenic structures (earthworks) from a DEM.

Method mirrors what archaeologists actually do with LiDAR DEMs:

  1. Local Relief Model (LRM): DEM minus a smoothed DEM. This removes the
     broad natural landscape (river valleys, regional slope) and leaves the
     small-amplitude local relief where earthworks live. (Hesse 2010.)

  2. Hillshade & slope for visualization / QA.

  3. Feature extraction on the LRM:
       - positive-relief blobs  -> candidate MOUNDS / platforms
       - closed rings of relief -> candidate GEOGLYPHS / ditched enclosures
     Candidates are scored by amplitude, size and geometric regularity, then
     the strongest are reported with lat/lon so they can be checked on imagery.

Everything downstream of `DEM` is resolution-agnostic: feed it a real
sub-meter bare-earth LiDAR DEM and the same code finds far smaller features.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import numpy as np
from scipy import ndimage

from dem_fetch import DEM


# ---- terrain derivatives ---------------------------------------------------

def hillshade(elev: np.ndarray, mpp: float, az: float = 315.0,
              alt: float = 45.0, z_factor: float = 1.0) -> np.ndarray:
    dy, dx = np.gradient(elev * z_factor, mpp)
    slope = np.pi / 2.0 - np.arctan(np.hypot(dx, dy))
    aspect = np.arctan2(-dx, dy)
    az_r, alt_r = np.radians(360.0 - az + 90.0), np.radians(alt)
    hs = (np.sin(alt_r) * np.sin(slope) +
          np.cos(alt_r) * np.cos(slope) * np.cos(az_r - aspect))
    return np.clip(hs, 0.0, 1.0)


def slope_deg(elev: np.ndarray, mpp: float) -> np.ndarray:
    dy, dx = np.gradient(elev, mpp)
    return np.degrees(np.arctan(np.hypot(dx, dy)))


def local_relief_model(elev: np.ndarray, mpp: float,
                       feature_scale_m: float = 300.0) -> np.ndarray:
    """LRM = elevation - low-pass(elevation). Sigma is set so the low-pass
    keeps landforms larger than roughly `feature_scale_m` and the residual
    isolates features around that scale and below."""
    sigma_px = max(1.0, (feature_scale_m / mpp) / 2.0)
    smooth = ndimage.gaussian_filter(elev, sigma=sigma_px, mode="nearest")
    return elev - smooth


# ---- candidate detection ---------------------------------------------------

@dataclass
class Candidate:
    lon: float
    lat: float
    row: int
    col: int
    kind: str            # "mound" | "ring"
    amplitude_m: float   # local relief amplitude
    diameter_m: float
    regularity: float    # 0..1, how compact/round the blob is
    score: float

    def to_dict(self):
        return asdict(self)


def _regularity(area_px: float, perimeter_px: float) -> float:
    """Isoperimetric compactness: 1.0 == perfect circle."""
    if perimeter_px <= 0:
        return 0.0
    return float(np.clip(4.0 * np.pi * area_px / (perimeter_px ** 2), 0.0, 1.0))


def detect(dem: DEM, feature_scale_m: float = 300.0,
           min_diameter_m: float = 80.0, max_diameter_m: float = 500.0,
           z_thresh: float = 2.0, max_candidates: int = 40) -> list[Candidate]:
    lrm = local_relief_model(dem.elev, dem.meters_per_px, feature_scale_m)

    # robust standardization (median / MAD) so a few outliers don't set scale
    med = np.median(lrm)
    mad = np.median(np.abs(lrm - med)) + 1e-6
    z = (lrm - med) / (1.4826 * mad)

    mpp = dem.meters_per_px
    min_area = np.pi * (0.5 * min_diameter_m / mpp) ** 2
    max_area = np.pi * (0.5 * max_diameter_m / mpp) ** 2

    cands: list[Candidate] = []
    # positive relief -> mounds/platforms ; negative relief -> ditched rings
    for sign, kind in ((+1.0, "mound"), (-1.0, "ring")):
        mask = (sign * z) > z_thresh
        # clean speckle
        mask = ndimage.binary_opening(mask, iterations=1)
        labels, n = ndimage.label(mask)
        if n == 0:
            continue
        objs = ndimage.find_objects(labels)
        for idx in range(1, n + 1):
            comp = labels == idx
            area = float(comp.sum())
            if area < min_area or area > max_area:
                continue
            sl = objs[idx - 1]
            perim = _perimeter(comp[sl])
            reg = _regularity(area, perim)
            if reg < 0.35:                       # reject stringy/natural shapes
                continue
            cy, cx = ndimage.center_of_mass(comp)
            amp = float(np.abs(lrm[comp]).mean())
            diam = 2.0 * np.sqrt(area / np.pi) * mpp
            peak_z = float((sign * z)[comp].max())
            score = peak_z * reg * np.log1p(amp)
            lon, lat = dem.rowcol_to_lonlat(cy, cx)
            cands.append(Candidate(lon=round(lon, 6), lat=round(lat, 6),
                                   row=int(cy), col=int(cx), kind=kind,
                                   amplitude_m=round(amp, 2),
                                   diameter_m=round(diam, 1),
                                   regularity=round(reg, 3),
                                   score=round(float(score), 3)))
    cands.sort(key=lambda c: c.score, reverse=True)
    return cands[:max_candidates]


def _perimeter(binary: np.ndarray) -> float:
    er = ndimage.binary_erosion(binary)
    return float((binary & ~er).sum())


def save_candidates(cands: list[Candidate], path: str) -> None:
    features = [{
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [c.lon, c.lat]},
        "properties": {k: v for k, v in c.to_dict().items()
                       if k not in ("lon", "lat")},
    } for c in cands]
    fc = {"type": "FeatureCollection", "features": features}
    with open(path, "w") as f:
        json.dump(fc, f, indent=2)

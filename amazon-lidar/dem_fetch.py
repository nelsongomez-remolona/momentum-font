"""
Fetch a Digital Elevation Model (DEM) for an Amazon bounding box.

Source: AWS "Terrain Tiles" open dataset (Terrarium PNG encoding), a public,
key-free mirror of global elevation data (SRTM 1-arc-second / 3-arc-second,
plus other sources). Docs: https://registry.opendata.aws/terrain-tiles/

IMPORTANT RESOLUTION CAVEAT
---------------------------
This is ~30 m/pixel *surface* elevation data, not sub-meter airborne LiDAR,
and it is NOT canopy-removed bare-earth. Real Amazonian archaeology (e.g.
Prumers et al. 2022, Nature) uses <1 m LiDAR DEMs classified to ground returns.
At 30 m you can only resolve *large* earthworks -- the Acre "geoglyphs" and
Llanos de Mojos causeways/mounds that are 100-300 m across. This pipeline is
built so that swapping in a real bare-earth LiDAR GeoTIFF (see load_geotiff)
runs the exact same detection with no changes.
"""

from __future__ import annotations

import io
import json
import math
import os
import time
from dataclasses import dataclass, asdict

import numpy as np
import requests
from PIL import Image

TERRARIUM_URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
TILE_PX = 256


@dataclass
class BBox:
    """Geographic bounding box in decimal degrees (WGS84)."""
    west: float
    south: float
    east: float
    north: float

    def center(self) -> tuple[float, float]:
        return (0.5 * (self.south + self.north), 0.5 * (self.west + self.east))


@dataclass
class DEM:
    """A stitched elevation grid plus the georeferencing needed to map
    pixel (row, col) <-> (lat, lon)."""
    elev: np.ndarray            # (H, W) float32, meters
    bbox: BBox                  # geographic extent actually covered
    zoom: int
    meters_per_px: float        # approximate, at the box center latitude

    def rowcol_to_lonlat(self, row: float, col: float) -> tuple[float, float]:
        h, w = self.elev.shape
        lon = self.bbox.west + (col + 0.5) / w * (self.bbox.east - self.bbox.west)
        # rows increase southward (north at top)
        lat = self.bbox.north - (row + 0.5) / h * (self.bbox.north - self.bbox.south)
        return lon, lat


# ---- slippy-map tile math (Web Mercator) -----------------------------------

def _lonlat_to_tile(lon: float, lat: float, z: int) -> tuple[float, float]:
    n = 2.0 ** z
    xt = (lon + 180.0) / 360.0 * n
    lat_r = math.radians(lat)
    yt = (1.0 - math.asinh(math.tan(lat_r)) / math.pi) / 2.0 * n
    return xt, yt


def _tile_to_lonlat(xt: float, yt: float, z: int) -> tuple[float, float]:
    n = 2.0 ** z
    lon = xt / n * 360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi * (1.0 - 2.0 * yt / n))))
    return lon, lat


def _decode_terrarium(png_bytes: bytes) -> np.ndarray:
    img = np.asarray(Image.open(io.BytesIO(png_bytes)).convert("RGB")).astype(np.float64)
    # Terrarium: elevation = (R*256 + G + B/256) - 32768  (meters)
    elev = (img[..., 0] * 256.0 + img[..., 1] + img[..., 2] / 256.0) - 32768.0
    return elev.astype(np.float32)


def _fetch_tile(z: int, x: int, y: int, session: requests.Session,
                retries: int = 4) -> np.ndarray:
    url = TERRARIUM_URL.format(z=z, x=x, y=y)
    delay = 2.0
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=60)
            if r.status_code == 200:
                return _decode_terrarium(r.content)
            # tiles outside coverage return 404 -> treat as flat/no-data
            if r.status_code == 404:
                return np.zeros((TILE_PX, TILE_PX), dtype=np.float32)
        except requests.RequestException:
            pass
        time.sleep(delay)
        delay *= 2
    raise RuntimeError(f"failed to fetch tile {z}/{x}/{y} after {retries} tries")


def fetch_dem(bbox: BBox, zoom: int = 12, cache_dir: str | None = None,
              verbose: bool = True) -> DEM:
    """Download and stitch all terrarium tiles covering `bbox` at `zoom`.

    zoom 12 over the Amazon is ~30-40 m/px effective (source data is coarser
    than the tile grid, so higher zoom does not add real detail)."""
    x0f, y0f = _lonlat_to_tile(bbox.west, bbox.north, zoom)   # top-left
    x1f, y1f = _lonlat_to_tile(bbox.east, bbox.south, zoom)   # bottom-right
    x0, y0 = int(math.floor(x0f)), int(math.floor(y0f))
    x1, y1 = int(math.floor(x1f)), int(math.floor(y1f))
    nx, ny = (x1 - x0 + 1), (y1 - y0 + 1)
    if verbose:
        print(f"[dem] zoom {zoom}: {nx}x{ny} = {nx*ny} tiles "
              f"({nx*TILE_PX}x{ny*TILE_PX} px)")

    session = requests.Session()
    session.headers.update({"User-Agent": "amazon-lidar-demo/1.0"})
    mosaic = np.zeros((ny * TILE_PX, nx * TILE_PX), dtype=np.float32)

    for j, ty in enumerate(range(y0, y1 + 1)):
        for i, tx in enumerate(range(x0, x1 + 1)):
            tile = _tile_from_cache(cache_dir, zoom, tx, ty, session)
            mosaic[j*TILE_PX:(j+1)*TILE_PX, i*TILE_PX:(i+1)*TILE_PX] = tile
        if verbose:
            print(f"[dem] row {j+1}/{ny} done")

    # exact geographic extent of the stitched mosaic (tile-aligned)
    west, north = _tile_to_lonlat(x0, y0, zoom)
    east, south = _tile_to_lonlat(x1 + 1, y1 + 1, zoom)
    covered = BBox(west, south, east, north)

    clat, _ = covered.center()
    circ = 40075016.686
    mpp = circ * math.cos(math.radians(clat)) / (2.0 ** zoom) / TILE_PX
    return DEM(elev=mosaic, bbox=covered, zoom=zoom, meters_per_px=mpp)


def _tile_from_cache(cache_dir, z, x, y, session) -> np.ndarray:
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, f"{z}_{x}_{y}.npy")
        if os.path.exists(path):
            return np.load(path)
        tile = _fetch_tile(z, x, y, session)
        np.save(path, tile)
        return tile
    return _fetch_tile(z, x, y, session)


def save_dem(dem: DEM, path_stem: str) -> None:
    np.save(path_stem + ".npy", dem.elev)
    meta = {"bbox": asdict(dem.bbox), "zoom": dem.zoom,
            "meters_per_px": dem.meters_per_px, "shape": list(dem.elev.shape)}
    with open(path_stem + ".json", "w") as f:
        json.dump(meta, f, indent=2)


def load_geotiff(path: str) -> DEM:
    """Drop-in loader for a real bare-earth LiDAR DEM GeoTIFF (needs rasterio).
    Lets you run the identical detection on genuine <1 m data."""
    import rasterio  # optional dependency
    with rasterio.open(path) as src:
        elev = src.read(1).astype(np.float32)
        b = src.bounds
        bbox = BBox(b.left, b.bottom, b.right, b.top)
        mpp = abs(src.transform.a)
    return DEM(elev=elev, bbox=bbox, zoom=-1, meters_per_px=mpp)

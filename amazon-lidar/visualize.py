"""Render terrain products and a candidate overlay as PNGs (Pillow only)."""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

from dem_fetch import DEM
from detect import Candidate, hillshade, local_relief_model


def _norm(a: np.ndarray, lo_pct=2.0, hi_pct=98.0) -> np.ndarray:
    lo, hi = np.percentile(a, [lo_pct, hi_pct])
    if hi <= lo:
        hi = lo + 1e-6
    return np.clip((a - lo) / (hi - lo), 0.0, 1.0)


def _to_img(gray01: np.ndarray) -> Image.Image:
    return Image.fromarray((gray01 * 255).astype(np.uint8), mode="L").convert("RGB")


def _diverging(x: np.ndarray) -> Image.Image:
    """Blue(neg)-white(0)-red(pos) map for the Local Relief Model."""
    v = np.clip(x, -1.0, 1.0)
    r = np.clip(1.0 + v, 0, 1)
    g = 1.0 - np.abs(v)
    b = np.clip(1.0 - v, 0, 1)
    rgb = (np.stack([r, g, b], axis=-1) * 255).astype(np.uint8)
    return Image.fromarray(rgb, "RGB")


def render_all(dem: DEM, cands: list[Candidate], out_dir: str) -> dict:
    import os
    os.makedirs(out_dir, exist_ok=True)
    mpp = dem.meters_per_px

    hs = hillshade(dem.elev, mpp)
    lrm = local_relief_model(dem.elev, mpp)
    lrm_n = lrm / (np.percentile(np.abs(lrm), 98) + 1e-6)

    hs_img = _to_img(hs)
    lrm_img = _diverging(lrm_n)
    dem_img = _to_img(_norm(dem.elev))

    # overlay candidates on hillshade
    ov = hs_img.copy()
    draw = ImageDraw.Draw(ov)
    for c in cands:
        rpx = max(6, int(0.5 * c.diameter_m / mpp))
        color = (255, 60, 60) if c.kind == "mound" else (60, 160, 255)
        draw.ellipse([c.col - rpx, c.row - rpx, c.col + rpx, c.row + rpx],
                     outline=color, width=2)

    paths = {}
    for name, img in (("dem", dem_img), ("hillshade", hs_img),
                      ("lrm", lrm_img), ("candidates", ov)):
        p = f"{out_dir}/{name}.png"
        img.save(p)
        paths[name] = p
    return paths

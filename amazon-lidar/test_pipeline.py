"""Offline tests: tile math round-trips and detection finds a planted mound.
Run:  python test_pipeline.py    (no network required)
"""

import numpy as np

from dem_fetch import BBox, DEM, _lonlat_to_tile, _tile_to_lonlat
from detect import detect, local_relief_model


def test_tile_roundtrip():
    for lon, lat, z in [(-67.5, -9.9, 12), (-64.9, -14.5, 13), (0, 0, 8)]:
        xt, yt = _lonlat_to_tile(lon, lat, z)
        lon2, lat2 = _tile_to_lonlat(xt, yt, z)
        assert abs(lon - lon2) < 1e-6 and abs(lat - lat2) < 1e-6, (lon, lat, z)
    print("ok  tile round-trip")


def test_rowcol_mapping():
    dem = DEM(elev=np.zeros((100, 200), np.float32),
              bbox=BBox(-68, -10, -67, -9), zoom=12, meters_per_px=30.0)
    lon, lat = dem.rowcol_to_lonlat(0, 0)            # top-left pixel
    assert lon < -67.99 and lat > -9.01
    lon, lat = dem.rowcol_to_lonlat(99, 199)         # bottom-right pixel
    assert lon > -67.01 and lat < -9.99
    print("ok  row/col -> lon/lat mapping")


def test_detect_planted_mound():
    # flat ground + gentle regional tilt + one circular mound
    h = w = 400
    yy, xx = np.mgrid[0:h, 0:w]
    elev = 150.0 + 0.01 * xx                          # regional slope
    cy, cx, r = 200, 200, 4                           # ~120 m wide at 30 m/px
    mound = 4.0 * np.exp(-(((yy - cy) ** 2 + (xx - cx) ** 2) / (2 * r ** 2)))
    elev = (elev + mound).astype(np.float32)
    dem = DEM(elev=elev, bbox=BBox(-68, -10, -67, -9),
              zoom=12, meters_per_px=30.0)

    lrm = local_relief_model(dem.elev, 30.0)
    assert lrm[cy, cx] > 1.0                          # mound survives LRM

    cands = detect(dem, feature_scale_m=300, min_diameter_m=100,
                   max_diameter_m=800, z_thresh=2.0)
    assert cands, "no candidates found"
    top = cands[0]
    assert abs(top.row - cy) < 12 and abs(top.col - cx) < 12, (top.row, top.col)
    assert top.kind == "mound"
    print(f"ok  planted mound detected at row={top.row} col={top.col} "
          f"(truth {cy},{cx}), score={top.score}")


if __name__ == "__main__":
    test_tile_roundtrip()
    test_rowcol_mapping()
    test_detect_planted_mound()
    print("\nall tests passed")

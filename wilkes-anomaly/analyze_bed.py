#!/usr/bin/env python3
"""
Test the Wilkes Land gravity-anomaly hypotheses against sub-ice bed topography.

Pulls ETOPO 2022 *bedrock* elevation (which incorporates BedMachine Antarctica
under the ice) via NOAA THREDDS OPeNDAP, subsets the Wilkes Land window, and
asks a simple question: does the bedrock around the anomaly centre (70 S, 120 E)
show impact-crater morphology (raised circular rim + central peak) or just a
subglacial tectonic basin?

Run:  python3 analyze_bed.py   (needs xarray, netCDF4, pydap, numpy, matplotlib)
Source: NOAA NCEI ETOPO 2022, 60 arc-second bedrock
        https://www.ncei.noaa.gov/products/etopo-global-relief-model
"""
import numpy as np, xarray as xr
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

URL = ("https://www.ngdc.noaa.gov/thredds/dodsC/global/ETOPO2022/60s/"
       "60s_bed_elev_netcdf/ETOPO_2022_v1_60s_N90W180_bed.nc")
C_LAT, C_LON = -70.0, 120.0            # Wilkes Land anomaly centre

def great_circle_km(la, lo):
    R = 6371.0
    p1, p2 = np.radians(C_LAT), np.radians(la)
    dl = np.radians(lo - C_LON)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))

def main():
    z = xr.open_dataset(URL)["z"].sel(lat=slice(-80, -60), lon=slice(95, 145)).load()
    lat, lon = z.lat.values, z.lon.values
    LON, LAT = np.meshgrid(lon, lat)
    Z = z.values
    D = great_circle_km(LAT, LON)
    land = LAT < -66                    # exclude the ocean margin to the north

    print("Radial bed profile from the anomaly centre (grounded bed, lat<-66):")
    print(f"{'r (km)':>9}{'mean m':>9}{'p10':>7}{'p90':>7}")
    for lo, hi in [(0, 60), (60, 120), (120, 180), (180, 240), (240, 300)]:
        m = (D >= lo) & (D < hi) & land
        v = Z[m]
        print(f"{lo:>4}-{hi:<4}{np.nanmean(v):>9.0f}{np.nanpercentile(v,10):>7.0f}"
              f"{np.nanpercentile(v,90):>7.0f}")
    core = (D < 250) & land
    print(f"\nWithin 250 km: {100*np.mean(Z[core]<0):.0f}% below sea level, "
          f"mean {np.nanmean(Z[core]):.0f} m")
    print("Impact test -> central 0-60 km vs 60-120 km ring: "
          f"{np.nanmean(Z[(D<60)&land]):.0f} m vs {np.nanmean(Z[(D>=60)&(D<120)&land]):.0f} m "
          "(a central PEAK would make the centre higher; here it is flat).")

    fig, ax = plt.subplots(figsize=(11, 7), dpi=130)
    im = ax.pcolormesh(lon, lat, Z, cmap="terrain",
                       norm=TwoSlopeNorm(vmin=-3000, vcenter=0, vmax=1500), shading="auto")
    plt.colorbar(im, ax=ax, label="Bed elevation (m, sub-ice)")
    ax.plot(C_LON, C_LAT, "r*", ms=18, mec="k", label="Anomaly centre (70°S,120°E)")
    th = np.linspace(0, 2 * np.pi, 200)
    for rkm, st in [(240, "r-"), (120, "r--")]:
        dlat = rkm / 111.0
        dlon = rkm / (111.0 * np.cos(np.radians(C_LAT)))
        ax.plot(C_LON + dlon * np.cos(th), C_LAT + dlat * np.sin(th), st, lw=1.6,
                label=f"{2*rkm:.0f} km circle")
    ax.contour(lon, lat, Z, levels=[0], colors="k", linewidths=0.6)
    ax.set(xlabel="Longitude (°E)", ylabel="Latitude (°)", ylim=(-80, -62),
           title="ETOPO 2022 bedrock (sub-ice) — Wilkes Land anomaly region")
    ax.legend(loc="lower left", fontsize=8, framealpha=.9)
    plt.tight_layout(); plt.savefig("wilkes_map.png")
    print("\nSaved wilkes_map.png")


if __name__ == "__main__":
    main()

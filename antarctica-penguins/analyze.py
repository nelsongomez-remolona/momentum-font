#!/usr/bin/env python3
"""
Antarctic penguin colony anomaly analysis.

Data: Antarctic Penguin Biogeography Project (MAPPPD), Che-Castaldo et al.
      Breeding-colony counts for six penguin species south of 60 S, 1892-2022.
      Source: https://github.com/CCheCastaldo/mapppdr  (CC-BY 4.0)
      Paper:  https://doi.org/10.3897/BDJ.11.e101476

Run:  python3 analyze.py
Deps: pandas  (the CSVs in ./data were exported from the package's .rda files)
"""
import pandas as pd

DATA = "data/"

def load():
    obs = pd.read_csv(DATA + "penguin_obs.csv")
    sites = pd.read_csv(DATA + "sites.csv")
    # Breeding pairs = nest counts; keep real, present, non-future observations.
    d = obs[(obs.type == "nests") & (obs.presence == 1)
            & (obs["count"] > 0) & (obs.year <= 2023)].copy()
    d = d.merge(sites[["site_id", "site_name", "region", "latitude"]],
                on="site_id", how="left")
    return d


def colony_trend(g, min_span=15, min_years=3, min_size=50):
    """Early-vs-late mean nest count for one colony. Returns %% change or None."""
    g = g.sort_values("year")
    if g.year.max() - g.year.min() < min_span or g.year.nunique() < min_years:
        return None
    early = g[g.year <= g.year.quantile(.34)]["count"].mean()
    late = g[g.year >= g.year.quantile(.66)]["count"].mean()
    if early < min_size:            # drop tiny colonies (percentages are noise)
        return None
    return pd.Series({
        "first": int(g.year.min()), "last": int(g.year.max()),
        "early": round(early), "late": round(late),
        "pct": 100 * (late - early) / early,
        "lat": round(g.latitude.iloc[0], 1),
        "region": g.region.iloc[0], "name": g.site_name.iloc[0],
    })


def trends(d, species_id):
    return (d[d.species_id == species_id]
            .groupby("site_id").apply(colony_trend, include_groups=False)
            .dropna(how="all").dropna(subset=["pct"]))


def main():
    d = load()

    print("=" * 68)
    print("1. WHO IS WINNING AND LOSING  (colonies with >=15 yr, >=50 nests)")
    print("=" * 68)
    for spid, label in [("ADPE", "Adelie"), ("CHPE", "Chinstrap"),
                        ("GEPE", "Gentoo"), ("EMPE", "Emperor")]:
        tr = trends(d, spid)
        if len(tr) == 0:
            continue
        print(f"{label:10s} colonies={len(tr):3d}  "
              f"increasing={100*(tr.pct>0).mean():3.0f}%  "
              f"decreasing={100*(tr.pct<0).mean():3.0f}%  "
              f"median={tr.pct.median():+5.0f}%")

    print("\n" + "=" * 68)
    print("2. ADELIE CLIMATE DIVIDE  (same species, opposite fate by latitude)")
    print("=" * 68)
    a = trends(d, "ADPE")
    north, south = a[a.lat > -66], a[a.lat <= -70]
    print(f"North of 66S (warm Peninsula):  median {north.pct.median():+.0f}%  "
          f"n={len(north)}, declining={100*(north.pct<0).mean():.0f}%")
    print(f"South of 70S (cold continent):  median {south.pct.median():+.0f}%  "
          f"n={len(south)}, increasing={100*(south.pct>0).mean():.0f}%")

    print("\n" + "=" * 68)
    print("3. SPECIES SWAP  (chinstrap down >20% AND gentoo up >20% at same rock)")
    print("=" * 68)
    c, g = trends(d, "CHPE")[["pct"]], trends(d, "GEPE")[["pct"]]
    swap = c.join(g, lsuffix="_ch", rsuffix="_ge", how="inner")
    swap = swap[(swap.pct_ch < -20) & (swap.pct_ge > 20)]
    sites = pd.read_csv(DATA + "sites.csv")[["site_id", "site_name"]]
    print(swap.merge(sites, left_index=True, right_on="site_id")
              .sort_values("pct_ge", ascending=False)
              [["site_name", "pct_ch", "pct_ge"]].round(0).to_string(index=False))

    print("\n" + "=" * 68)
    print("4. HEADLINE EXTREMES")
    print("=" * 68)
    ch = trends(d, "CHPE").sort_values("pct")
    ge = trends(d, "GEPE").sort_values("pct", ascending=False)
    print("Worst chinstrap collapse:", ch.iloc[0]["name"],
          f"{ch.iloc[0].early:.0f}->{ch.iloc[0].late:.0f} nests ({ch.iloc[0].pct:+.0f}%)")
    print("Biggest gentoo boom:     ", ge.iloc[0]["name"],
          f"{ge.iloc[0].early:.0f}->{ge.iloc[0].late:.0f} nests ({ge.iloc[0].pct:+.0f}%)")


if __name__ == "__main__":
    main()

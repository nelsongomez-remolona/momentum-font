# antarctica-penguins

Anomaly analysis of Antarctic penguin breeding colonies, using the
**Antarctic Penguin Biogeography Project (MAPPPD)** database — every published
colony count for six penguin species south of 60°S, 1892–2022.

- **[FINDINGS.md](./FINDINGS.md)** — what the data says + the surprising anomalies.
- **[analyze.py](./analyze.py)** — reproducible analysis (`python3 analyze.py`, needs `pandas`).
- **[data/](./data)** — CSVs exported from the source R package.

## Data provenance
- Che-Castaldo et al. (2024), *Biodiversity Data Journal*,
  [doi:10.3897/BDJ.11.e101476](https://doi.org/10.3897/BDJ.11.e101476)
- Source package (CC-BY 4.0): <https://github.com/CCheCastaldo/mapppdr>
- `data/*.csv` were converted from that package's `.rda` files (unmodified values).

## Files in `data/`
| file | rows | description |
|---|---:|---|
| `penguin_obs.csv` | 5,483 | colony counts (site, species, year, type, count, vantage) |
| `sites.csv` | 729 | colony locations (lat/lon, region) |
| `species.csv` | 7 | species codes ↔ common/scientific names |
| `site_species.csv` | 918 | which species breed at which site |

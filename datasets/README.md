# Learning Datasets

A curated collection of datasets that teach the most about the world, money, risk,
health, people, resources, geography, and science. All files retrieved 2026-07-21.

Analysis scripts: `fun-numbers.py` (batch 1), `fun-numbers-2.py` (batch 2).

## owid/ — Our World in Data
Source: https://ourworldindata.org/grapher/<slug>.csv

| File | What it is |
|---|---|
| `life-expectancy.csv` | Life expectancy at birth, by country, 1543–present |
| `child-mortality.csv` | Share of children dying before age 5, by country |
| `share-of-population-in-extreme-poverty.csv` | Share living under the international poverty line |
| `co2-emissions-per-capita.csv` | Per-capita CO₂ emissions, by country |
| `literacy-rates.csv` | Adult literacy rates, cross-country historical |

## worldbank/ — World Bank Open Data
Source: https://api.worldbank.org/v2/en/indicator/<code>?downloadformat=csv

- `gdp-per-capita/` — NY.GDP.PCAP.CD (GDP per capita, current US$)
- `life-expectancy/` — SP.DYN.LE00.IN (life expectancy at birth)

## fred/ — Federal Reserve Economic Data
Source: https://fred.stlouisfed.org/graph/fredgraph.csv?id=<series>

| Series | What it is |
|---|---|
| `CPIAUCSL` | Consumer Price Index, all urban consumers (1947–) |
| `UNRATE` | Unemployment rate (1948–) |
| `MEHOINUSA672N` | Real median household income (1984–) |
| `CSUSHPINSA` | Case-Shiller US national home price index (1987–) |
| `FEDFUNDS` | Federal funds effective rate (1954–) |
| `AHETPI` | Avg hourly earnings, production/nonsupervisory workers (1964–) |

## bls-cex/ — BLS Consumer Expenditure Survey (via FRED mirrors)
BLS.gov blocks this environment's proxy, so the CXU series were pulled from FRED,
which mirrors the official CEX tables. Annual data, 1984–.

- `CXUTOTALEXPLB0101M`–`0106M` — total average annual expenditures: all consumer
  units, then income quintiles lowest → highest
- `CXUINCBEFTXLB0101M/0102M/0106M` — income before taxes: all units, lowest
  quintile, highest quintile
- `CXUFOODTOTLLB0101M`, `CXUHOUSINGLB0101M` — food and housing spending, all units

## cdc-mortality/ — CDC / NCHS causes of death
- `nchs-leading-causes-of-death.csv` — deaths and age-adjusted death rates for the
  10 leading causes, US + states, 1999–2017.
  Source: https://data.cdc.gov/api/views/bi63-dtpu/rows.csv

## ssa-life-tables/ — Social Security actuarial life table
SSA.gov blocks this environment's proxy; retrieved via Internet Archive snapshot
(2024-01-01) of https://www.ssa.gov/oact/STATS/table4c6.html — the 2020 period
life table.

- `ssa-period-life-table.html` — original page
- `ssa-period-life-table-2020.csv` — parsed: age, death probability, survivors
  per 100k, and remaining life expectancy, by sex, ages 0–119

## noaa-nasa-climate/ — Global temperature record
- `gistemp-global-monthly.csv` — NASA GISTEMP v4 global land+ocean temperature
  anomalies (°C vs 1951–1980 mean), monthly, 1880–present.
  Source: https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv

## opportunity-atlas/ — Opportunity Insights
- `county_outcomes_simple.csv` — mean adult household income rank (and
  incarceration rate) for children who grew up in each US county, by parent income
  percentile, race, and gender. `kfr_pooled_pooled_p25` = mean income rank in
  adulthood for kids raised at the 25th parent-income percentile.
  Source: https://opportunityinsights.org/data/

## gss/ — General Social Survey (NORC), 1972–2024
- `GSS_stata.zip` — official cumulative release R3a (Stata format + codebook PDFs)
- `gss-extract-1972-2024.csv` — compact extract (75,699 respondents × 20
  variables: happiness, trust, politics, attitudes, income, weights) pulled from
  the Stata file for easy pandas use
- `gss-extract-codebook.txt` — variable and value labels for the extract.
  Values ≥ 2147483625 are GSS missing-data sentinels (don't know / not asked / etc.)

## fivethirtyeight/ — FiveThirtyEight datasets
Source: https://github.com/fivethirtyeight/data

- `US_births_1994-2003_CDC_NCHS.csv`, `US_births_2000-2014_SSA.csv` — daily US births
- `bad-drivers.csv` — state-level collision/insurance data
- `candy-data.csv` — Halloween candy matchup win rates
- `bechdel-movies.csv` — 1,794 films: Bechdel test result, budget, gross

---

# Batch 2: resources, geography, science

## owid-energy/ — OWID Energy Dataset
- `owid-energy-data.csv` — every country since 1900: energy production/consumption
  by source, electricity mix, per-capita figures.
  Source: https://github.com/owid/energy-data

## usgs-minerals/ — USGS Mineral Commodity Summaries 2025
Source: ScienceBase item 677eaf95d34e760b392c4970 (official 2025 data release v2.0)

- `world/MCS2025_World_Data.csv` — world mine production and reserves by
  commodity and country, 2023–2024
- `salient/` — per-commodity US salient statistics (production, imports,
  price, net import reliance), ~85 commodities

## faostat-crops/ — Crop yields (FAO data via OWID graphers)
- `cereal-yield.csv` — cereal yield (t/ha) by country, 1961–
- `key-crop-yields.csv` — yields for ~10 major crops by country, 1961–

## water/ — Freshwater (AQUASTAT/OWID)
- `annual-freshwater-withdrawals.csv` — total withdrawals by country (m³/yr)
- `freshwater-use-by-sector.csv` — global freshwater use, 1901–

## usgs-earthquakes/ — USGS Earthquake Catalog
- `earthquakes-m6plus-1900-present.csv` — every recorded M6.0+ earthquake,
  1900–present (time, location, depth, magnitude).
  Source: https://earthquake.usgs.gov/fdsnws/event/1/

## natural-earth/ — Natural Earth 110m vectors
- `ne_110m_admin_0_countries.zip`, `ne_110m_populated_places.zip` — country
  polygons and major cities (shapefiles, public domain).
  Source: https://naciscdn.org/naturalearth/

## geonames/ — GeoNames
- `cities1000.zip` — all ~140k populated places with >1,000 people: name,
  coordinates, elevation, population, country (tab-separated inside zip).
  Source: https://download.geonames.org/export/dump/

## population-demography/ — UN World Population Prospects (via OWID graphers)
- `population.csv` — population by country, 10,000 BCE–2100 (projections)
- `median-age.csv` — median age by country incl. UN projections
- `fertility-rate.csv` — children per woman by country, 1800s–

## noaa-co2/ — Keeling Curve (NOAA Global Monitoring Laboratory)
- `co2_mm_mlo.csv` — monthly mean atmospheric CO₂ at Mauna Loa, 1958–
- `co2_weekly_mlo.csv` — weekly means, 1974–
  Source: https://gml.noaa.gov/ccgg/trends/

## nasa-exoplanets/ — NASA Exoplanet Archive
- `exoplanets.csv` — all confirmed exoplanets (pscomppars table): name, host
  star, discovery method/year, orbital period, radius, mass, equilibrium temp,
  stellar properties, distance.
  Source: https://exoplanetarchive.ipac.caltech.edu/ (TAP query)

## Not retrievable from this environment
- **CDC WONDER** interactive queries (POST-only API; the NCHS leading-causes file
  above covers the same ground)
- **BLS.gov and SSA.gov direct downloads** (proxy blocked; mirrored via FRED and
  the Internet Archive as noted above)

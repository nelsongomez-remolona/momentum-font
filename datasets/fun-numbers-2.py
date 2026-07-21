"""Fun numbers, batch 2: resources, geography, science. Run from datasets/."""
import zipfile

import numpy as np
import pandas as pd

D = {}

# --- 1. Energy transition (OWID) ---
e = pd.read_csv("owid-energy/owid-energy-data.csv")
world = e[e.country == "World"].set_index("year")
sw = (world.solar_share_elec + world.wind_share_elec).dropna()
D["solar+wind % of world electricity 2000 -> latest"] = (round(sw.loc[2000], 2), sw.index[-1], round(sw.iloc[-1], 1))
solar = world.solar_electricity.dropna()
D["world solar generation TWh 2010 -> latest (x)"] = (solar.loc[2010], solar.iloc[-1], round(solar.iloc[-1] / solar.loc[2010], 1))
coal = world.coal_consumption.dropna()
D["world coal peak year"] = (coal.idxmax(), "still >= 95% of peak?" , coal.iloc[-1] >= 0.95 * coal.max())
latest = e[(e.year == e.year.max() - 1) & e.iso_code.notna() & (e.population > 1e6)]
pc = latest.dropna(subset=["energy_per_capita"]).set_index("country").energy_per_capita
D["energy per capita kWh: top3, bottom3"] = (pc.nlargest(3).round(0).to_dict(), pc.nsmallest(3).round(0).to_dict())

# --- 2. Who controls the minerals (USGS MCS 2025) ---
m = pd.read_csv("usgs-minerals/world/MCS2025_World_Data.csv", encoding="utf-8-sig")
m.columns = [c.strip().replace(" ", "") for c in m.columns]
prod_col = [c for c in m.columns if c.startswith("PROD_EST")][0]
for commodity, key in [("Lithium", "lithium"), ("Cobalt", "cobalt"), ("Rare earths", "rare earths"), ("Copper", "copper")]:
    sub = m[m.COMMODITY.str.contains(commodity, case=False, na=False)].copy()
    if sub.TYPE.str.contains("Mine", case=False, na=False).any():
        sub = sub[sub.TYPE.str.contains("Mine", case=False, na=False)]
    sub[prod_col] = pd.to_numeric(sub[prod_col], errors="coerce")
    sub["RESERVES_2024"] = pd.to_numeric(sub["RESERVES_2024"], errors="coerce")
    countries = sub[~sub.COUNTRY.str.contains("World|Other", case=False, na=False)]
    wtot = sub[sub.COUNTRY.str.contains("World", case=False, na=False)][prod_col].max()
    if countries[prod_col].notna().any() and pd.notna(wtot):
        top = countries.loc[countries[prod_col].idxmax()]
        D[f"{key}: top producer 2024 (share of world)"] = (top.COUNTRY, f"{100 * top[prod_col] / wtot:.0f}%")
        wres = sub[sub.COUNTRY.str.contains("World", case=False, na=False)]["RESERVES_2024"].max()
        if pd.notna(wres):
            D[f"{key}: 'years left' at current production"] = round(wres / wtot)

# --- 3. Feeding the world (FAO via OWID) ---
cy = pd.read_csv("faostat-crops/cereal-yield.csv")
wy = cy[cy.Entity == "World"].set_index("Year").iloc[:, -1]
D["world cereal yield t/ha 1961 -> latest (x)"] = (round(wy.loc[1961], 2), round(wy.iloc[-1], 2), round(wy.iloc[-1] / wy.loc[1961], 1))
last_yr = cy.Year.max()
best = cy[(cy.Year == last_yr) & cy.Code.notna() & (cy.Entity != "World")].nlargest(3, cy.columns[-1])
D[f"best national cereal yields {last_yr}"] = best[["Entity", cy.columns[-1]]].round(1).values.tolist()
majors = cy[(cy.Year == last_yr) & cy.Entity.isin(["Netherlands", "Germany", "France", "United States", "India", "Nigeria"])]
D["cereal yields, major farm economies"] = majors[["Entity", cy.columns[-1]]].round(1).values.tolist()

# --- 4. Water (AQUASTAT via OWID) ---
wu = pd.read_csv("water/freshwater-use-by-sector.csv")
gw = wu[wu.Entity == "World"].set_index("Year").iloc[:, -1].dropna()
D["global freshwater use 1901 -> latest (x)"] = (gw.index[0], gw.index[-1], round(gw.iloc[-1] / gw.iloc[0], 1))
fw = pd.read_csv("water/annual-freshwater-withdrawals.csv")
pop = pd.read_csv("population-demography/population.csv")
pop.columns = ["Entity", "Code", "Year", "pop"]
fw_last = fw[fw.Code.notna() & (fw.Entity != "World")].sort_values("Year").groupby("Entity").last().reset_index()
merged = fw_last.merge(pop[pop.Year == 2023], on="Entity", suffixes=("", "_p"))
merged["m3_per_person"] = merged.iloc[:, 3] / merged["pop"]
big = merged[merged["pop"] > 1e6]
D["freshwater withdrawals m3/person/yr: top 3"] = big.nlargest(3, "m3_per_person")[["Entity", "m3_per_person"]].round(0).values.tolist()

# --- 5. Earthquakes (USGS) ---
q = pd.read_csv("usgs-earthquakes/earthquakes-m6plus-1900-present.csv", parse_dates=["time"])
D["M6+ quakes recorded"] = len(q)
c67 = ((q.mag >= 6) & (q.mag < 7)).sum()
c78 = ((q.mag >= 7) & (q.mag < 8)).sum()
c8 = (q.mag >= 8).sum()
D["Gutenberg-Richter: M6-7 / M7-8 / M8+"] = (c67, c78, c8, f"ratios {c67/c78:.1f}x, {c78/c8:.1f}x")
D["biggest quakes ever recorded"] = q.nlargest(4, "mag")[["time", "place", "mag"]].astype(str).values.tolist()
rec = q[q.time.dt.year >= 1970]
D["avg M6+ per year (since 1970)"] = round(len(rec) / (rec.time.dt.year.max() - 1969), 0)
D["energy: M9.5 vs M6.0 (x)"] = f"{10 ** (1.5 * 3.5):,.0f}"

# --- 6. Cities of the world (GeoNames) ---
cols = ["geonameid", "name", "asciiname", "altnames", "lat", "lon", "fclass", "fcode",
        "country", "cc2", "a1", "a2", "a3", "a4", "population", "elevation", "dem", "tz", "mod"]
with zipfile.ZipFile("geonames/cities1000.zip") as z:
    cities = pd.read_csv(z.open("cities1000.txt"), sep="\t", names=cols, low_memory=False)
D["settlements with pop>1000"] = len(cities)
bigc = cities[cities.population > 100000].copy()
bigc["alt"] = bigc.elevation.fillna(bigc.dem)
hi = bigc.nlargest(3, "alt")
D["highest cities >100k people (m)"] = hi[["name", "country", "alt"]].values.tolist()
D["most common city names"] = cities.name.value_counts().head(5).to_dict()
D["northernmost city >100k"] = bigc.nlargest(1, "lat")[["name", "country", "lat"]].values.tolist()

# --- 7. Demography (UN WPP via OWID) ---
ma = pd.read_csv("population-demography/median-age.csv")
macol = "Median age"
ma_now = ma[(ma.Year == 2023) & ma.Code.notna() & (ma.Code != "") & (ma.Entity != "World")]
ma_now = ma_now[~ma_now.Entity.str.contains(r"\(", regex=True)].dropna(subset=[macol])
D["median age 2023: youngest, oldest"] = (
    ma_now.nsmallest(2, macol)[["Entity", macol]].round(1).values.tolist(),
    ma_now.nlargest(2, macol)[["Entity", macol]].round(1).values.tolist())
fr = pd.read_csv("population-demography/fertility-rate.csv")
frcol = fr.columns[-1]
wfr = fr[fr.Entity == "World"].set_index("Year")[frcol].dropna()
D["world fertility 1963 -> latest"] = (round(wfr.loc[1963], 1), round(wfr.iloc[-1], 2))
kr = fr[fr.Entity == "South Korea"].set_index("Year")[frcol].dropna()
D["South Korea fertility 1960 -> latest"] = (round(kr.loc[1960], 1), round(kr.iloc[-1], 2))

# --- 8. Keeling curve (NOAA) ---
co2 = pd.read_csv("noaa-co2/co2_mm_mlo.csv", comment="#")
co2 = co2[co2.average > 0]
D["CO2 ppm first-year avg (1959) -> last-12mo avg"] = (
    round(co2[co2.year == 1959].average.mean(), 1), round(co2.tail(12).average.mean(), 1))
by_decade = co2.groupby(co2.year // 10 * 10).average.agg(["first", "last"])
D["CO2 growth ppm/yr: 1960s vs 2015-25"] = (
    round((co2[co2.year == 1970].average.mean() - co2[co2.year == 1960].average.mean()) / 10, 2),
    round((co2.tail(12).average.mean() - co2[co2.year == co2.year.max() - 10].average.mean()) / 10, 2))
recent = co2[co2.year == co2.year.max() - 1]
D["Earth 'breathing': seasonal CO2 swing (ppm)"] = round(recent.average.max() - recent.average.min(), 1)

# --- 9. Exoplanets (NASA) ---
x = pd.read_csv("nasa-exoplanets/exoplanets.csv")
D["confirmed exoplanets"] = len(x)
D["discovery methods"] = x.discoverymethod.value_counts().head(4).to_dict()
D["known before 2000 vs since 2015"] = ((x.disc_year < 2000).sum(), (x.disc_year >= 2015).sum())
r = x.pl_rade.dropna()
gap = pd.cut(r, [1.0, 1.5, 1.8, 2.1, 3.0]).value_counts().sort_index()
D["radius gap (planets per bin, Earth radii)"] = {str(k): int(v) for k, v in gap.items()}
near = x.dropna(subset=["sy_dist"]).nsmallest(1, "sy_dist")
D["closest exoplanet"] = near[["pl_name", "sy_dist"]].values.tolist()[0] + ["parsecs"]
hot = x.dropna(subset=["pl_eqt"]).nlargest(1, "pl_eqt")
D["hottest planet (equilibrium temp K)"] = hot[["pl_name", "pl_eqt"]].values.tolist()[0]
fast = x.dropna(subset=["pl_orbper"]).nsmallest(1, "pl_orbper")
D["shortest year (days)"] = fast[["pl_name", "pl_orbper"]].values.tolist()[0]

for k, v in D.items():
    print(f"{k}: {v}")

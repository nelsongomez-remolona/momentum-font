"""Crunch fun numbers across the learning datasets. Run from datasets/."""
import pandas as pd
import numpy as np

pd.set_option("display.width", 200)
D = {}

# --- 1. Life expectancy (OWID) ---
le = pd.read_csv("owid/life-expectancy.csv")
le.columns = ["entity", "code", "year", "le"]
w = le[le.entity == "World"].set_index("year")["le"]
D["world life expectancy 1950 -> latest"] = (w.loc[1950], w.index.max(), w.iloc[-1])
for c in ["India", "South Korea", "United States"]:
    s = le[le.entity == c].set_index("year")["le"]
    D[f"life expectancy {c} 1950 -> latest"] = (s.loc[1950], s.iloc[-1])

# --- 2. Extreme poverty (OWID) ---
pov = pd.read_csv("owid/share-of-population-in-extreme-poverty.csv")
pcol = [c for c in pov.columns if "share" in c.lower() or "poverty" in c.lower()][-1]
wp = pov[pov.Entity == "World"].dropna(subset=[pcol]).set_index("Year")[pcol]
D["world extreme poverty % first -> last"] = (wp.index.min(), wp.iloc[0], wp.index.max(), wp.iloc[-1])

# --- 3. Child mortality (OWID) ---
cm = pd.read_csv("owid/child-mortality.csv")
ccol = cm.columns[-1]
for c in ["World", "United States"]:
    s = cm[cm.Entity == c].dropna(subset=[ccol]).set_index("Year")[ccol]
    D[f"child mortality % {c} 1900ish -> latest"] = (s.index.min(), s.iloc[0], s.index.max(), s.iloc[-1])

# --- 4. Inflation & wages (FRED) ---
cpi = pd.read_csv("fred/CPIAUCSL.csv", parse_dates=["observation_date"]).set_index("observation_date").iloc[:, 0]
D["$100 in 1970 = today"] = 100 * cpi.iloc[-1] / cpi.loc["1970-01-01"]
D["$100 in 1990 = today"] = 100 * cpi.iloc[-1] / cpi.loc["1990-01-01"]
wage = pd.read_csv("fred/AHETPI.csv", parse_dates=["observation_date"]).set_index("observation_date").iloc[:, 0]
j = pd.concat([cpi, wage], axis=1, keys=["cpi", "w"]).dropna()
real = j.w / j.cpi
D["real wage growth 1973 -> now (%)"] = 100 * (real.iloc[-1] / real.loc["1973-01-01"] - 1)
D["real wage growth 1996 -> now (%)"] = 100 * (real.iloc[-1] / real.loc["1996-01-01"] - 1)

# --- 5. Home prices vs CPI (FRED) ---
hp = pd.read_csv("fred/CSUSHPINSA.csv", parse_dates=["observation_date"]).set_index("observation_date").iloc[:, 0]
start = "1987-01-01"
D["home prices x since 1987"] = hp.iloc[-1] / hp.loc[start]
D["CPI x since 1987"] = cpi.iloc[-1] / cpi.loc[start]

# --- 6. Your odds (SSA life table) ---
lt = pd.read_csv("ssa-life-tables/ssa-period-life-table-2020.csv").set_index("age")
D["odds 30yo dies this year (M, F)"] = (f"1 in {1/lt.loc[30,'male_death_prob']:.0f}",
                                        f"1 in {1/lt.loc[30,'female_death_prob']:.0f}")
D["odds 70yo dies this year (M, F)"] = (f"1 in {1/lt.loc[70,'male_death_prob']:.0f}",
                                        f"1 in {1/lt.loc[70,'female_death_prob']:.0f}")
D["% of newborns reaching 90 (M, F)"] = (lt.loc[90, "male_lives"] / 1000, lt.loc[90, "female_lives"] / 1000)
D["% of 65yos reaching 90 (M, F)"] = (100 * lt.loc[90, "male_lives"] / lt.loc[65, "male_lives"],
                                      100 * lt.loc[90, "female_lives"] / lt.loc[65, "female_lives"])

# --- 7. What actually kills people (CDC/NCHS) ---
cdc = pd.read_csv("cdc-mortality/nchs-leading-causes-of-death.csv")
us17 = cdc[(cdc.State == "United States") & (cdc.Year == 2017) & (cdc["Cause Name"] != "All causes")]
D["top causes of death US 2017"] = us17.nlargest(5, "Deaths")[["Cause Name", "Deaths"]].values.tolist()

# --- 8. Warming (NASA GISTEMP) ---
g = pd.read_csv("noaa-nasa-climate/gistemp-global-monthly.csv", skiprows=1, na_values="***")
g["J-D"] = pd.to_numeric(g["J-D"], errors="coerce")
ann = g.set_index("Year")["J-D"].dropna()
D["warmest 10 years on record"] = ann.nlargest(10).index.tolist()
D["anomaly 1880s avg vs last-5yr avg (C)"] = (ann.loc[1880:1889].mean(), ann.iloc[-5:].mean())

# --- 9. Where kids rise (Opportunity Atlas) ---
oa = pd.read_csv("opportunity-atlas/county_outcomes_simple.csv")
oa = oa[oa.pooled_pooled_count > 10000].copy()  # big counties only
best = oa.nlargest(5, "kfr_pooled_pooled_p25")[["czname", "kfr_pooled_pooled_p25"]]
worst = oa.nsmallest(5, "kfr_pooled_pooled_p25")[["czname", "kfr_pooled_pooled_p25"]]
D["best counties for poor kids (income rank at ~35)"] = best.values.tolist()
D["worst counties for poor kids"] = worst.values.tolist()

# --- 10. GSS: happiness, trust, weed ---
gss = pd.read_csv("gss/gss-extract-1972-2024.csv")
MISS = 2_000_000_000  # GSS sentinel codes are ~2.1e9
def clean(col):
    s = gss[["year", col]].copy()
    s = s[s[col] < MISS]
    return s
tr = clean("trust")
tr["can_trust"] = (tr.trust == 1).astype(float)
trust_by_yr = tr.groupby("year").can_trust.mean() * 100
D["'most people can be trusted' % (first yr, latest yr)"] = (
    trust_by_yr.index[0], round(trust_by_yr.iloc[0], 1), trust_by_yr.index[-1], round(trust_by_yr.iloc[-1], 1))
hp2 = clean("happy")
hp2["very_happy"] = (hp2.happy == 1).astype(float)
hap = hp2.groupby("year").very_happy.mean() * 100
D["'very happy' % (first, latest)"] = (hap.index[0], round(hap.iloc[0], 1), hap.index[-1], round(hap.iloc[-1], 1))
gr = clean("grass")
gr["legal"] = (gr.grass == 1).astype(float)
grs = gr.groupby("year").legal.mean() * 100
D["support marijuana legalization % (first, latest)"] = (
    grs.index[0], round(grs.iloc[0], 1), grs.index[-1], round(grs.iloc[-1], 1))

# --- 11. Friday the 13th (FiveThirtyEight births) ---
b = pd.read_csv("fivethirtyeight/US_births_1994-2003_CDC_NCHS.csv")
b2 = pd.read_csv("fivethirtyeight/US_births_2000-2014_SSA.csv")
births = pd.concat([b[b.year < 2000], b2])
f13 = births[(births.day_of_week == 5) & (births.date_of_month == 13)].births.mean()
f_other = births[(births.day_of_week == 5) & (births.date_of_month.isin([6, 20]))].births.mean()
D["births Fri 13th vs adjacent Fridays"] = (f13, f_other, 100 * (f13 / f_other - 1))
wk = births.groupby("day_of_week").births.mean()
D["avg births weekday vs weekend"] = (wk.loc[1:5].mean(), wk.loc[6:7].mean())

# --- 12. Candy & Bechdel ---
candy = pd.read_csv("fivethirtyeight/candy-data.csv")
D["top 3 candies"] = candy.nlargest(3, "winpercent")[["competitorname", "winpercent"]].values.tolist()
bd = pd.read_csv("fivethirtyeight/bechdel-movies.csv")
D["bechdel pass rate 1970s vs 2010s (%)"] = (
    100 * (bd[bd.year < 1980].binary == "PASS").mean(),
    100 * (bd[bd.year >= 2010].binary == "PASS").mean())

# --- 13. Spending vs income by quintile (CEX via FRED) ---
def fred_last(f):
    s = pd.read_csv(f"bls-cex/{f}.csv", parse_dates=["observation_date"]).set_index("observation_date").iloc[:, 0]
    return s.iloc[-1], s.index[-1].year
inc_lo, yr = fred_last("CXUINCBEFTXLB0102M")
exp_lo, _ = fred_last("CXUTOTALEXPLB0102M")
inc_hi, _ = fred_last("CXUINCBEFTXLB0106M")
exp_hi, _ = fred_last("CXUTOTALEXPLB0106M")
D[f"lowest quintile {yr}: income vs spending"] = (inc_lo, exp_lo)
D[f"highest quintile {yr}: income vs spending"] = (inc_hi, exp_hi)

for k, v in D.items():
    print(f"{k}: {v}")

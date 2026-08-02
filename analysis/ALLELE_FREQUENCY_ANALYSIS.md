# Allele-Frequency Analysis: Trait & Ancestry SNPs

*A hands-on analysis using **real downloaded data** — not textbook numbers.
Population allele frequencies were pulled live from the **Ensembl REST API**
(1000 Genomes Project, phase 3) for the specific genes discussed in this
repo's research thread, then tabulated and visualized.*

Run 2 August 2026. Reproducible via `analysis/fetch_freqs.py`.

![Allele frequency heatmap](allele_frequencies.svg)

---

## What was done

1. Queried `rest.ensembl.org/variation/human/<rsID>?pops=1` for 6 SNPs.
2. Extracted 1000 Genomes phase-3 frequencies of the trait-relevant
   ("highlight") allele for 9 populations, correcting for strand and
   distinguishing *absent* (0%) from *not-genotyped* (n/a).
3. Saved tidy data (`allele_frequencies.csv`), raw API responses
   (`raw_variation.json`), and a self-contained heatmap
   (`allele_frequencies.svg`).

**Important limitation up front:** 1000 Genomes contains **no Filipino
sample.** The nearest available proxies are **KHV (Kinh Vietnamese)** and
**CDX (Dai, southern China)** — both Southeast Asian, both carrying the
Austronesian-adjacent ancestry that dominates lowland Filipino genomes, but
neither is Filipino. Treat them as *directional*, not exact.

## The data

Frequency (%) of the highlighted allele, 1000 Genomes phase 3:

| Gene | Allele | Trait | KHV (Viet) | CDX (Dai) | CHB (Han) | JPT (Jpn) | EAS | SAS | EUR | AFR | PEL (Peru) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **ALDH2** | A | Alcohol flush | 13.6 | 4.3 | 16.0 | 24.0 | 17.4 | 0.0 | 0.0 | 0.2 | 0.6 |
| **ADH1B** | A | Fast alcohol metabolism | 64.6 | 63.4 | 70.9 | 73.1 | 69.7 | 2.0 | 2.9 | 0.2 | 1.2 |
| **EDAR** | G | Thick hair / shovel teeth | 82.3 | 89.8 | 93.7 | 80.3 | 87.3 | 1.3 | 1.1 | 0.3 | 75.9 |
| **ABCC11** | T | Dry earwax / less odor | 63.6 | 53.8 | 97.1 | 88.0 | 78.0 | 48.2 | 13.6 | 1.2 | 27.1 |
| **LCT/MCM6** | T | Lactase persistence | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 11.3 | 50.8 | 2.7 | 10.6 |
| **ACTN3** | T | R577X "sprint gene" (X=stop) | 40.9 | 50.5 | 42.2 | 48.6 | 44.3 | 58.7 | 43.4 | 11.5 | 75.3 |

## What the data shows

**1. Your lactose intolerance is right there in the numbers.**
The lactase-persistence allele (LCT/MCM6) is **literally 0.0% in every East
Asian population** sampled — Vietnamese, Dai, Han, Japanese — versus **50.8%
in Europeans.** This is the cleanest signal in the whole table, and it
matches exactly what you told me: adult lactose intolerance is the East/SE
Asian *default*, and the milk-drinking mutation is the European oddity. The
data confirms your lived experience.

**2. The East Asian / Austronesian "trait cluster" is strong in the Filipino
proxies.** In KHV and CDX (closest to Filipino):
- **EDAR** (thick straight hair, shovel-shaped incisors): **82–90%**, versus
  ~1% in Europeans, South Asians, and Africans. Near-defining.
- **ADH1B** fast alcohol metabolism: **~64%**, versus ~3% elsewhere.
- **ABCC11** dry earwax / reduced body odor: **54–64%** (and up to 97% in
  Han), versus 14% EUR and ~1% AFR.
These are the genetic fingerprints of the Austronesian ancestry layer we
discussed — and they're common in the populations nearest to yours.

**3. "Asian glow" (ALDH2) is real but milder in the SE-Asian proxies.**
The alcohol-flush allele runs **17% across East Asians** but is highest in
Japanese (24%) and Han (16%) and *lower* in the SE-Asian-adjacent CDX (4%) /
KHV (14%). Consistent with what I said earlier: flush is common in East Asia
but tends to be **less frequent toward island/SE Asia** — so a Filipino is
somewhat less likely to flush than a Han or Japanese person, though far more
likely than a European (0%).

**4. A bonus finding — the Asia→Americas connection lights up.**
Look at the **PEL (Peruvian)** column: EDAR **76%** and ACTN3-X **75%**,
tracking the East Asian pattern, because Indigenous Americans descend from
the same ancient East Eurasian population. The data quietly re-tells the
peopling of the Americas — the same migration story that runs through your
own ancestry.

**5. The "sprint gene" honesty check.** ACTN3 is the flattest row: the
nonfunctional X allele sits at 40–59% across Eurasians (your proxies ~41–51%)
— i.e., **hugely common and non-distinctive.** The one dramatic outlier is
**AFR at 11.5%** (Africans overwhelmingly keep the functional "R" sprint
allele). That's a real, replicated frequency difference — *and* it's the gene
we flagged earlier as having a **tiny effect size** (~1% of sprint variance).
So it's a perfect illustration of the whole thread's lesson: a striking
frequency gap that still explains almost nothing about who actually becomes
an athlete.

## Caveats

- **Proxies, not Filipinos.** KHV/CDX approximate the Austronesian layer but
  miss the deep Negrito/Denisovan component that makes Filipino ancestry
  distinctive. The Larena 2021 Ayta genomes (controlled-access) would be
  needed for that.
- **Allele frequency ≠ phenotype.** Carrying an allele is a probability, not
  a guarantee; most traits are polygenic and environment-shaped.
- **Not medical advice.** For anything actionable (e.g., G6PD, drug
  response), see a clinician and a validated test.

## Reproduce it

```bash
cd analysis
python3 fetch_freqs.py     # downloads from Ensembl -> CSV + raw JSON
python3 make_svg.py        # renders the heatmap SVG
```
No API key required; Ensembl REST is open.

# Allele-Frequency Analysis: Trait & Ancestry SNPs

*A hands-on analysis using **real downloaded data** — not textbook numbers.
Population allele frequencies were pulled live from the **Ensembl REST API**
(1000 Genomes Project, phase 3) for a panel of trait/ancestry genes spanning
diet, pigmentation, morphology, disease, and physical performance, then
tabulated and visualized.*

Run 3 August 2026 · **13 SNPs × 10 populations** · reproducible via
`analysis/fetch_freqs.py`.

![Allele frequency heatmap](allele_frequencies.svg)

---

## What was done

1. Queried `rest.ensembl.org/variation/human/<rsID>?pops=1` for 13 SNPs.
2. Extracted 1000 Genomes phase-3 frequencies of the trait-relevant
   ("highlight") allele for 10 populations, correcting for strand and
   distinguishing *absent* (0%) from *not-genotyped* (n/a).
3. Saved tidy data (`allele_frequencies.csv`), raw API responses
   (`raw_variation.json`), and a categorized heatmap
   (`allele_frequencies.svg`).

**Limitation up front:** 1000 Genomes has **no Filipino sample.** The nearest
proxies are **KHV (Kinh Vietnamese)** and **CDX (Dai, southern China)** — both
Southeast Asian, carrying the Austronesian-adjacent ancestry that dominates
lowland Filipino genomes, but neither is Filipino. Treat as *directional*.

## The data

Frequency (%) of the highlighted allele, 1000 Genomes phase 3:

| Cat | Gene | Allele | Trait | KHV | CDX | CHB | JPT | EAS | SAS | EUR | AFR | YRI | PEL |
|---|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Diet | **LCT/MCM6** | T | Lactase persistence | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 11.3 | 50.8 | 2.7 | 0.0 | 10.6 |
| Diet | **ALDH2** | A | Alcohol flush | 13.6 | 4.3 | 16.0 | 24.0 | 17.4 | 0.0 | 0.0 | 0.2 | 0.0 | 0.6 |
| Diet | **ADH1B** | A | Fast alcohol metabolism | 64.6 | 63.4 | 70.9 | 73.1 | 69.7 | 2.0 | 2.9 | 0.2 | 0.0 | 1.2 |
| Diet | **FADS1** | T | Fatty-acid (PUFA) metabolism | 81.8 | 78.0 | 35.4 | 32.7 | 56.6 | 13.7 | 34.7 | 2.2 | 0.9 | 80.6 |
| Pigment | **SLC24A5** | A | Light skin (West Eurasian) | 0.5 | 0.0 | 2.9 | 0.5 | 1.2 | 68.5 | 99.7 | 7.4 | 1.4 | 28.2 |
| Pigment | **SLC45A2** | G | Light skin (European) | 1.0 | 0.0 | 1.5 | 0.0 | 0.6 | 5.9 | 93.8 | 3.6 | 0.0 | 15.9 |
| Pigment | **HERC2/OCA2** | G | Blue eyes | 0.0 | 0.0 | 0.0 | 0.0 | 0.2 | 7.1 | 63.6 | 2.8 | 0.0 | 11.2 |
| Morphology | **EDAR** | G | Thick hair / shovel teeth | 82.3 | 89.8 | 93.7 | 80.3 | 87.3 | 1.3 | 1.1 | 0.3 | 0.0 | 75.9 |
| Morphology | **ABCC11** | T | Dry earwax / less odor | 63.6 | 53.8 | 97.1 | 88.0 | 78.0 | 48.2 | 13.6 | 1.2 | 0.0 | 27.1 |
| Disease | **HBB** | A | Sickle-cell (malaria) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 13.9 | 0.0 |
| Disease | **ACKR1** | C | Duffy-null (vivax malaria) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.6 | 96.4 | 99.5 | 4.1 |
| Disease | **APOL1** | G | APOL1 G1 (trypanosome) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 25.9 | 37.5 | 0.0 |
| Physical | **ACTN3** | T | R577X "sprint gene" (X=stop) | 40.9 | 50.5 | 42.2 | 48.6 | 44.3 | 58.7 | 43.4 | 11.5 | 8.8 | 75.3 |

## Key findings

**1. Your lactose intolerance is literally 0.0%.** The lactase-persistence
allele is absent from every East Asian population sampled, vs. 50.8% in
Europeans — matching your lived experience exactly.

**2. The Austronesian / East-Asian trait cluster** (EDAR 82–90%, ADH1B ~64%,
ABCC11 54–64% in the Filipino proxies) is strong and near-absent elsewhere.

**3. "Asian glow" fades toward SE Asia.** ALDH2 flush is 24% in Japanese but
just 4.3% in Dai — the population nearest to Filipino sits at the low end.

**4. FADS1 (new) splits East Asia in two.** The shown fatty-acid-metabolism
allele is **~80% in the Filipino proxies (KHV/CDX) and Peru**, but only
~33–35% in Han/Japanese — the SE-Asian proxies group with the Americas, not
with Northeast Asia. Diet-adaptation genes cut across the "East Asian" label.

**5. Pigmentation is the cleanest ancestry story — and the best proof "race"
isn't one gene.** Light skin via **SLC24A5 (99.7% EUR)** and **SLC45A2 (93.8%
EUR)** and blue eyes via **HERC2 (63.6% EUR)** are essentially West-Eurasian.
Yet East Asians — also light-skinned — carry these at **~1%**: they evolved
light skin through *different* genes. Same trait, separate genetic routes.

**6. Malaria/disease genes are sharply African** — Duffy-null **96–99%**
(the sharpest single-allele divide in the whole panel), sickle-cell 10–14%,
APOL1-G1 26–38% — all ~0% elsewhere. These are local pathogen adaptations,
not general "racial" differences.

**7. The Americas connection recurs.** PEL tracks East Asian ancestry (EDAR
76%) but pushes some alleles to extremes via drift (ACTN3-X **75%**, the
highest anywhere).

**8. Honesty check holds.** ACTN3 (the "sprint gene") remains the flattest,
least-distinctive row across Eurasia — the gene with a ~1% effect size on
performance. Big frequency gaps, tiny real-world meaning.

## Caveats

- **Proxies, not Filipinos.** KHV/CDX miss the deep Negrito/Denisovan layer
  (needs the controlled-access Ayta genomes).
- **No highland/Oceanian samples in 1000G**, so the Tibetan-EPAS1 and
  Papuan/Ayta-Denisovan stories can't be shown here — flagged rather than
  faked.
- **Allele frequency ≠ phenotype**; most traits are polygenic. Not medical
  advice.
- **Ascertainment bias:** some markers (e.g. the European lactase SNP) were
  discovered in Europeans and undercount adaptations elsewhere.

## Reproduce it

```bash
cd analysis
python3 fetch_freqs.py     # downloads from Ensembl -> CSV + raw JSON
python3 make_svg.py        # renders the heatmap SVG
```
No API key required; Ensembl REST is open.

# Open Data Directory

Curated, mostly-free datasets spanning the threads in this repo — drowned
Sundaland (bathymetry), archaic humans (Denisovan/Neanderthal), modern
population genetics (incl. Philippine/Ayta), trait & pharmacogenomic
variants, and the tools to explore them.

**Access legend:**
🟢 **Open** — download directly, no application.
🟡 **Controlled** — free, but human-subjects data requires a data-access
application and ethics agreement (this is normal and appropriate for
identifiable human genomes).

---

## 1. Archaic humans — Denisovan & Neanderthal genomes

- 🟢 **Denisovan genome (high-coverage, ~30×)** — Max Planck Institute for
  Evolutionary Anthropology. Freely downloadable, no password (also mirrored
  on AWS). → https://www.eva.mpg.de/genetics/genome-projects/denisova/
- 🟢 **Altai Neanderthal genome** — Max Planck EVA. Free (observe the Ft.
  Lauderdale principles). → https://www.eva.mpg.de/neandertal/
- 🟢 **Allen Ancient DNA Resource (AADR)** — the curated compendium of *all*
  published ancient human genomes (v66, 2026: ~17,600 ancient + ~6,400 modern
  individuals at >1M SNPs), with geographic/temporal metadata. Harvard
  Dataverse, permanent DOI.
  → https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/FFIDCW
  → Reich Lab: https://reich.hms.harvard.edu/datasets
  → Interactive map (AADR Visualizer): https://arcg.is/1CyL5n

## 2. Modern population genetics (global, incl. Asia & the Philippines)

- 🟡 **Larena et al. 2021 — Philippine genomes** (118 ethnic groups, 25
  Negrito populations incl. the record-Denisovan Ayta Magbukon; ~2.3M SNPs).
  Data associated with the PNAS + Current Biology papers; genotype data via
  the authors' repository / on request.
  → PNAS: https://www.pnas.org/doi/10.1073/pnas.2026132118
  → Current Biology (Ayta/Denisovan): https://www.cell.com/current-biology/fulltext/S0960-9822(21)00977-5
- 🟡 **GenomeAsia 100K** — whole genomes from 219 population groups across 64
  Asian countries. Browser is open; raw data via EGA (accession
  EGAS00001002921).
  → Browser: https://browser.genomeasia100k.org/
  → Project: https://www.genomeasia100k.org/
  → EGA: https://ega-archive.org/studies/EGAS00001002921
- 🟢 **1000 Genomes Project** — the foundational open reference panel of human
  variation (incl. East/Southeast Asian samples). Fully public.
  → https://www.internationalgenome.org/
- 🟢 **Simons Genome Diversity Project (SGDP)** — high-coverage genomes from
  ~300 diverse populations. → https://reich.hms.harvard.edu/datasets
- 🟢 **Human Genome Diversity Project (HGDP)** — classic worldwide diversity
  panel. → https://www.internationalgenome.org/data-portal/data-collection/hgdp

## 3. Variant & allele-frequency data (for specific genes)

Use these to look up frequencies of the genes discussed here — EPAS1
(altitude), ACTN3 (sprint), MSTN (muscle), ALDH2 (alcohol flush), EDAR
(hair/teeth), G6PD, HLA, etc., across populations.

- 🟢 **gnomAD** (Genome Aggregation Database) — allele frequencies from
  hundreds of thousands of people across ancestry groups; browse or download
  VCFs. → https://gnomad.broadinstitute.org/
- 🟢 **Ensembl — population genetics** — allele frequencies/genotypes pulling
  from 1000 Genomes, gnomAD, etc.
  → https://www.ensembl.org/info/genome/variation/species/populations.html
- 🟢 **NHGRI-EBI GWAS Catalog** — curated genotype→trait associations.
  Gene pages, e.g.:
  → EPAS1: https://www.ebi.ac.uk/gwas/genes/EPAS1
  → ACTN3: https://www.ebi.ac.uk/gwas/genes/ACTN3
- 🟢 **PharmGKB** + **CPIC** — pharmacogenomics: variant → drug-response
  (HLA-B\*15:02/carbamazepine, CYP2C19/clopidogrel, G6PD triggers), with
  clinical guidelines. → https://www.pharmgkb.org/ · https://cpicpgx.org/
- 🟢 **ALFRED** (Yale ALlele FREquency Database) — anthropologically-oriented
  population allele frequencies. → https://alfred.med.yale.edu/

## 4. Sundaland — bathymetry & paleogeography

- 🟢 **GEBCO gridded bathymetry** — global ocean+land elevation grid
  (GEBCO_2026, 15 arc-sec). Download whole or subset the Sunda Shelf.
  → https://www.gebco.net/data-products/gridded-bathymetry-data
  → Download portal: https://download.gebco.net/
- 🟢 **OpenTopography — GEBCO global bathymetry/topography** (programmatic
  access). → https://portal.opentopography.org/
- 🟢 **NOAA NCEI bathymetry / ETOPO** — alternative global relief models.
  → https://www.ncei.noaa.gov/products/etopo-global-relief-model
- 📄 **Palaeodrainages of the Sunda Shelf (2024)** — reconstruction methods &
  maps built on GEBCO contours.
  → https://www.sciencedirect.com/science/article/pii/S2095383624001184

## 5. Why some data is "controlled" (and that's fine)

Identifiable human genomes — especially from small Indigenous populations
like the Ayta — are held under **managed access** for good reasons: consent,
privacy, and Indigenous data sovereignty. Applying (via EGA/dbGaP or the
authors) is free and routine for researchers; it exists to protect the people
whose DNA it is, not to hide the science. Aggregate/summary resources
(gnomAD, GWAS Catalog, Ensembl) give you most of the population-level answers
with no application at all.

---

*Compiled 2 August 2026. Access URLs and dataset versions change over time —
verify the current release on each source's site.*

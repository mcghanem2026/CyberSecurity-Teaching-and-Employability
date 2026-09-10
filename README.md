# CyBOK-informed analysis of UK cyber-security degrees: processed data and code

Processed data, reference tables and reproduction scripts for

> Ghanem, M. C., Hills, L., Patel, P. and de Quincey, E. (under review). *Necessary but not sufficient: A CyBOK-informed
> documentary analysis of curriculum, certification and graduate employability in UK cyber security degrees.*
> Manuscript submitted to the *International Journal of Educational Research*.

The study maps the documented, credit-bearing content of 51 NCSC-certified UK cyber-security programmes
(41 master's, 10 bachelor's/integrated) onto the five broad categories of the Cyber Security Body of Knowledge
(CyBOK v1.1) and compares that "supply" profile with two reference points: the knowledge profiles of four
professional certifications (CISSP, SSCP, CISM, CRISC) and a transparent, certification- and skills-dictionary-derived
employer-demand proxy for the "Big Four" professional-services firms.

## What is (and is not) in this repository

**Included — processed data as reported in the paper**

| file | content | paper |
|---|---|---|
| `data/processed/corpus_summary.csv` | corpus composition (n by level and provider type; zero-HOR count) | §3.2, §4.1 |
| `data/processed/mean_category_shares_by_group.csv` | mean re-normalised category shares: master's, bachelor's, Russell Group, other | Table 4 |
| `data/processed/demand_proxy_big_four_aggregate.csv` | Big Four demand proxy, mean supply and category gaps | Table 6 / Table 7 |
| `data/processed/firm_level_gaps_vs_bachelors_supply.csv` | gaps (proxy − bachelor's supply) for each of the four firms | Figure 7 |
| `data/processed/programme_similarity_illustrative.csv` | cosine similarity of four illustrative master's programmes (P1–P4) | Figure 2 |
| `data/reference/certification_profiles_cybok_categories.csv` | CISSP / SSCP / CISM / CRISC profiles on the five categories (from the CyBOK Mapping Booklet v2.2) | Table 5 |
| `data/reference/cybok_v1.1_knowledge_areas_to_categories.csv` | the 21 CyBOK v1.1 Knowledge Areas → five broad categories used for coding | Table 3 |
| `data/reference/post2024_ai_security_evidence_sources.csv` | verified sources and data points behind §2.4 and §5.4 (AI security / governance gap) | §2.4, §5.4 |
| skills dictionary and demand-proxy files (see dedicated section below) | competency→KA weights, role-family weights, certification anchors, calibrated blend and firm mix | §3.4 |

**Not included**

- **Raw programme documentation** (programme specifications, module catalogues, credit schedules). These are
  institutional documents subject to licensing terms; they were summarised and aggregated, not reproduced.
- **The programme-level category-share dataset** (51 rows). Individual providers are not identified in the paper and
  the file is available from the corresponding author on reasonable request. Its header is given in
  `data/schema/`, and `scripts/compute_gaps_and_hhi.py` will process a file in that format if placed at
  `data/processed/programme_category_shares.csv`.
Every number in `data/processed/` and `data/reference/` is either a value reported in the manuscript, a documented
public reference value, or an output of the released scripts as described below.

## Skills dictionary and demand-proxy specification

The demand proxy is built from the certification profiles and a skills dictionary that maps commonly advertised
cyber-security competencies to CyBOK Knowledge Areas, weighted by the role families (governance and risk; security
operations; application security) into which the Big Four recruit graduates. The full specification is released:

| file | content |
|---|---|
| `data/reference/skills_dictionary.csv` | 28 commonly advertised competencies → CyBOK v1.1 Knowledge Areas, weights summing to 1 per competency (long form) |
| `data/reference/skills_dictionary_category_weights.csv` | the dictionary collapsed to the five broad categories via the KA→category map (generated) |
| `data/reference/role_family_competency_weights.csv` | competency weights for the three role families (each sums to 1) |
| `data/reference/role_family_certification_anchors.csv` | certification anchors per role family (CISM/CRISC/CISSP for governance and risk; CISSP/SSCP for operations and application security) |
| `data/processed/role_family_blend.csv` | certification/dictionary blend per role family (calibrated) |
| `data/processed/firm_role_family_mix.csv` | role-family mix per firm, floor 10 % per family (calibrated) |
| `data/processed/demand_proxy_firm_profiles.csv` | resulting firm-level proxy profiles (generated) |

`scripts/build_demand_proxy.py` combines these as: role-family profile = blend × certification anchors + (1 − blend) ×
dictionary; firm profile = Σ mix × role-family profiles; aggregate proxy = mean of the four firms; gap = firm profile −
mean bachelor's supply. The competency and role-family weights are specified from the public scope of each CyBOK v1.1
Knowledge Area and the competencies named in the paper. The blend and mix parameters are calibrated by constrained least
squares to the firm-level profiles reported in Figure 7; the script prints the residuals (maximum absolute deviation
0.023 at firm level and per category at aggregate level against Table 6).

## Reproducing the figures and derived quantities

```bash
pip install -r scripts/requirements.txt
python scripts/compute_gaps_and_hhi.py   # re-derives the gaps, checks them against the reported values,
                                         # recovers indicative firm-level demand profiles (2 d.p.)
python scripts/make_figures.py           # regenerates the six data figures as vector PDFs in figures/
python scripts/build_demand_proxy.py     # rebuilds the demand proxy from the dictionary and reports the fit
```

## Method in brief

Documentary, mixed-methods design (Bowen, 2009): credit-bearing content apportioned across the five CyBOK categories in
proportion to documented content; general-introductory credit set aside and the five substantive shares re-normalised to
sum to one; breadth measured by the Herfindahl–Hirschman Index (lower = broader); demand modelled by a transparent proxy
rather than a vacancy count; gaps = proxy share − mean supply share (positive = relative under-provision by degrees).
See `docs/methods_summary.md` and `docs/codebook.md`.

## Licence

Data (`data/`) and documentation: CC BY 4.0 (see `DATA_LICENSE`). Code (`scripts/`): MIT (see `LICENSE`).
Certification profiles derive from the CyBOK Mapping Booklet v2.2 (© Crown Copyright 2024, CyBOK project); CyBOK
Knowledge Area names are those of CyBOK v1.1 (University of Bristol / NCSC).

## Citation

See `CITATION.cff`. Please cite the paper when using the data.

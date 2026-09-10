# Data provenance and processing

## Supply side (degree programmes)
Population: UK degree programmes certified by the NCSC, supplemented by closely related programmes at the same providers
where documented alongside the certified award. Inclusion required publicly available documentation (programme
specifications, module catalogues, credit schedules) sufficient to apportion credit across CyBOK Knowledge Areas.
Coding: single primary coder with an independently double-coded reliability subset; multi-category modules apportioned by
documented content; introductory credit excluded and shares re-normalised across the five substantive categories.
Only aggregates are released (see `processed/`).

## Reference point 1: certifications
Knowledge profiles of CISSP, SSCP (ISC2) and CISM, CRISC (ISACA) expressed on the five broad categories, taken from the
CyBOK Mapping Booklet v2.2 (2024): https://www.cybok.org/media/downloads/CyBOK_MappingBookletv2.2_2024.pdf

## Reference point 2: Big Four employer-demand proxy
Constructed from (i) the certification profiles above and (ii) a skills dictionary mapping commonly advertised
cyber-security competencies to CyBOK categories, weighted by the role families (governance and risk; security operations;
application security) into which Deloitte, EY, KPMG and PwC recruit graduates. It is a proxy for professionally codified
demand, not a vacancy count, and is weighted towards the governance-heavy practice of large advisory firms.
Released as reported: the aggregate proxy (`processed/demand_proxy_big_four_aggregate.csv`) and the per-firm gaps
(`processed/firm_level_gaps_vs_bachelors_supply.csv`, 2 d.p.). The dictionary specification (`reference/skills_dictionary.csv`,
`reference/role_family_competency_weights.csv`, `reference/role_family_certification_anchors.csv`) and the calibrated blend
and firm mix (`processed/role_family_blend.csv`, `processed/firm_role_family_mix.csv`) are documented in the repository
README, section "Skills dictionary and demand-proxy specification", and rebuilt by `scripts/build_demand_proxy.py`.

## Post-2024 AI-security evidence (`reference/post2024_ai_security_evidence_sources.csv`)
Sources and data points used to argue that CyBOK v1.1 lags sector requirements on AI security, agentic-AI security and
AI governance. Every entry was checked against the publisher's or awarding body's own page in September 2026.

## Conventions
- Category order everywhere: Infrastructure Security; Software & Platform Security; Attacks & Defences; Systems Security;
  Human, Organisational & Regulatory Aspects.
- Shares are proportions summing to 1 (up to rounding); gaps are proxy − supply (positive = under-provision by degrees).
- Group means in Table 4 and the supply means in the gap pipeline (Table 6) differ by ≤ 0.005 (master's) and ≤ 0.017
  (bachelor's) because they were computed in separate pipelines; both are released as reported.

# Codebook

| variable | file(s) | type | definition |
|---|---|---|---|
| `cybok_category` | all category tables | text | one of the five CyBOK v1.1 broad categories (see `data/reference/cybok_v1.1_knowledge_areas_to_categories.csv`) |
| `*_share` / group columns | `mean_category_shares_by_group.csv`, `demand_proxy_big_four_aggregate.csv`, `certification_profiles_cybok_categories.csv` | proportion [0,1] | share of re-normalised, credit-bearing content (degrees), of examined knowledge (certifications) or of implied demand (proxy); each column sums to 1 |
| `gap_masters`, `gap_bachelors` | `demand_proxy_big_four_aggregate.csv` | signed proportion | demand-proxy share − mean supply share; positive = degrees under-provide relative to the proxy |
| firm rows | `firm_level_gaps_vs_bachelors_supply.csv` | signed proportion (2 d.p.) | firm-specific proxy share − mean bachelor's supply share |
| `P1`–`P4` | `programme_similarity_illustrative.csv` | [0,1] | cosine similarity of the five-category share vectors of four anonymised master's programmes spanning research-intensive and post-1992 providers |
| `n_programmes` | `corpus_summary.csv` | integer | count of programme records in the group |
| HHI (computed) | `scripts/compute_gaps_and_hhi.py` | [0.2,1] for k = 5 | Σ sᵢ², sum of squared category shares; lower = broader coverage; reported directly (the complement 1 − HHI is not used) |
| `competency`, `knowledge_area`, `weight` | `skills_dictionary.csv` | text, text, [0,1] | mapping of an advertised competency to CyBOK v1.1 Knowledge Areas; weights sum to 1 per competency |
| `role_family`, `competency`, `weight` | `role_family_competency_weights.csv` | text, text, [0,1] | competency mix of a role family (`governance_and_risk`, `security_operations`, `application_security`); sums to 1 per family |
| `role_family`, `certification`, `weight` | `role_family_certification_anchors.csv` | text, text, [0,1] | certification anchors per role family; sums to 1 per family |
| `certification_dictionary_blend` | `role_family_blend.csv` | [0,1] | calibrated weight on certification anchors (1 − weight on the competency dictionary) per role family |
| role-family columns | `firm_role_family_mix.csv` | simplex, floor 0.10 | calibrated share of each role family in a firm's graduate intake profile |


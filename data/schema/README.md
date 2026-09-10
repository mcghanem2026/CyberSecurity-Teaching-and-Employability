# Programme-level file (template only)

`programme_category_shares.TEMPLATE.csv` gives the header of the programme-level dataset
(51 rows in the study). The file itself is **not** released here: it is available from the
corresponding author on reasonable request (see the paper's Data Availability statement).

| column | meaning |
|---|---|
| `programme_id` | anonymised code (P1 … P51) |
| `level` | `masters` (MSc/MSci/MEng) or `bachelors_integrated` |
| `provider_type` | `russell_group` or `other` |
| `foundational_share_excluded` | share of credit set aside as general-introductory before re-normalisation |
| five category columns | re-normalised shares summing to 1 across the five substantive CyBOK categories |

Place a file with this header at `data/processed/programme_category_shares.csv` and
`scripts/compute_gaps_and_hhi.py` will compute per-programme HHI, group means and the
pairwise cosine-similarity matrix from it.

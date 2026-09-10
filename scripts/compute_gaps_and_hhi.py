#!/usr/bin/env python3
"""Recompute the derived quantities reported in the paper from the processed data.

- gaps = demand-proxy share - mean supply share (per category), checked against the reported values
- firm-level demand profiles recovered from the reported firm gaps (gap + bachelor's supply; 2 d.p., indicative)
- if data/processed/programme_category_shares.csv is present (not released; see data/schema/README.md):
  per-programme HHI, group means, share of programmes with zero HOR credit, pairwise cosine similarity
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data" / "processed"
CATS = ["Infrastructure Security", "Software & Platform Security", "Attacks & Defences",
        "Systems Security", "Human Organisational & Regulatory Aspects"]

def check_gaps():
    d = pd.read_csv(P / "demand_proxy_big_four_aggregate.csv").set_index("cybok_category")
    for lvl in ["masters", "bachelors"]:
        recomputed = (d["demand_proxy_share"] - d[f"{lvl}_supply_share"]).round(3)
        diff = (recomputed - d[f"gap_{lvl}"]).abs().max()
        print(f"[gaps] {lvl}: max |recomputed - reported| = {diff:.3f}")
    print(d.round(3).to_string(), "\n")
    return d

def recover_firm_profiles(d):
    g = pd.read_csv(P / "firm_level_gaps_vs_bachelors_supply.csv").set_index("firm")
    prof = g.add(d["bachelors_supply_share"].values, axis=1).round(2)
    prof["row_sum"] = prof.sum(axis=1).round(2)
    print("[firms] indicative demand profiles recovered from reported gaps (2 d.p.; sums may differ from 1 by rounding)")
    print(prof.to_string(), "\n")

def hhi(shares: np.ndarray) -> np.ndarray:
    """Herfindahl-Hirschman index: sum of squared category shares (lower = broader, more even coverage)."""
    return (shares ** 2).sum(axis=1)

def cosine_matrix(x: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(x, axis=1, keepdims=True)
    return (x @ x.T) / (n @ n.T)

def programme_level():
    f = P / "programme_category_shares.csv"
    if not f.exists():
        print("[programme-level] programme_category_shares.csv not present (not released; available on request) - skipped")
        return
    df = pd.read_csv(f)
    X = df[CATS].to_numpy(float)
    assert np.allclose(X.sum(axis=1), 1, atol=0.01), "shares must sum to 1 across the five categories"
    df["hhi"] = hhi(X)
    print("[programme-level] HHI: min %.3f (broadest) / max %.3f (most concentrated)" % (df.hhi.min(), df.hhi.max()))
    print(df.groupby("level")[CATS].mean().round(3).T.to_string())
    print(df.groupby("provider_type")[CATS].mean().round(3).T.to_string())
    zero = (df["Human Organisational & Regulatory Aspects"] == 0).sum()
    print(f"programmes with zero HOR credit: {zero} of {len(df)} ({100*zero/len(df):.1f}%)")
    S = pd.DataFrame(cosine_matrix(X), index=df.programme_id, columns=df.programme_id)
    S.round(3).to_csv(P / "programme_similarity_full.csv")
    print("wrote programme_similarity_full.csv")

if __name__ == "__main__":
    d = check_gaps()
    recover_firm_profiles(d)
    programme_level()

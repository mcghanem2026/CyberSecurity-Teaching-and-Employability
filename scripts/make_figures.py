#!/usr/bin/env python3
"""Regenerate the data figures of the paper from the processed CSVs (house style: serif, colour-blind-safe palette,
three-decimal annotations). Outputs vector PDFs to figures/.

  fig_degree_certs.pdf   degrees vs certification profiles (masters | bachelors)
  fig_demand_supply.pdf  Big Four demand proxy vs mean supply
  fig_mismatch.pdf       category gaps (proxy - supply)
  fig_firm_gaps.pdf      firm-level gaps heat map
  fig_rg_post92.pdf      Russell Group vs other providers (exploratory)
  fig_similarity.pdf     cosine similarity of four illustrative programmes
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
P, R, OUT = ROOT / "data" / "processed", ROOT / "data" / "reference", ROOT / "figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"], "pdf.fonttype": 42, "font.size": 9})
PAL = ["#1F4E8C", "#E39A57", "#5FA88E", "#9C7BB9", "#B8925A", "#8A8A8A"]   # colour-blind-safe house palette
LABELS = ["Infrastructure", "Software &\nPlatform", "Attacks &\nDefences", "Systems", "Human, Org.\n& Regulatory"]

def grouped_bars(ax, series: dict, title=None, ylabel="Share (sums to 1)", annotate=True):
    k, n = len(series), len(LABELS); w = 0.8 / k; x = np.arange(n)
    for i, (name, vals) in enumerate(series.items()):
        b = ax.bar(x - 0.4 + w * (i + 0.5), vals, w, label=name, color=PAL[i % len(PAL)], edgecolor="white", lw=0.5)
        if annotate:
            for r, v in zip(b, vals):
                ax.text(r.get_x() + r.get_width() / 2, v + 0.008, f"{v:.3f}", ha="center", va="bottom", fontsize=5.5, rotation=90)
    ax.set_xticks(x); ax.set_xticklabels(LABELS, fontsize=8); ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    if title: ax.set_title(title, fontsize=10)
    ax.legend(frameon=False, fontsize=7.5, ncol=min(k, 3), loc="upper left")

def fig_degree_certs():
    m = pd.read_csv(P / "mean_category_shares_by_group.csv")
    c = pd.read_csv(R / "certification_profiles_cybok_categories.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for ax, col, ttl in [(axes[0], "masters_n41", "(a) Master's programmes"), (axes[1], "bachelors_n10", "(b) Bachelor's / integrated")]:
        s = {"Degrees (mean)": m[col].values, **{k: c[k].values for k in ["CISSP", "SSCP", "CISM", "CRISC"]}}
        grouped_bars(ax, s, ttl, "Share of coverage (re-normalised)")
    axes[0].set_ylim(0, 0.9); fig.tight_layout(); fig.savefig(OUT / "fig_degree_certs.pdf"); plt.close(fig)

def fig_demand_supply():
    d = pd.read_csv(P / "demand_proxy_big_four_aggregate.csv")
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    grouped_bars(ax, {"Big Four demand (proxy)": d.demand_proxy_share.values, "Master's supply (mean)": d.masters_supply_share.values,
                      "Bachelor's supply (mean)": d.bachelors_supply_share.values})
    ax.set_ylim(0, 0.58); fig.tight_layout(); fig.savefig(OUT / "fig_demand_supply.pdf"); plt.close(fig)

def fig_mismatch():
    d = pd.read_csv(P / "demand_proxy_big_four_aggregate.csv")
    fig, ax = plt.subplots(figsize=(7.5, 3.8)); x = np.arange(5); w = 0.38
    for i, (col, name) in enumerate([("gap_masters", "Master's"), ("gap_bachelors", "Bachelor's")]):
        v = d[col].values
        b = ax.bar(x - w/2 + i*w, v, w, label=name, color=PAL[i], edgecolor="white")
        for r, val in zip(b, v):
            ax.text(r.get_x() + r.get_width()/2, val + (0.01 if val >= 0 else -0.01), f"{val:+.3f}", ha="center",
                    va="bottom" if val >= 0 else "top", fontsize=6.5)
    ax.axhline(0, color="black", lw=0.8); ax.set_xticks(x); ax.set_xticklabels(LABELS, fontsize=8)
    ax.set_ylabel("Gap (demand proxy − supply)"); ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8); ax.set_ylim(-0.29, 0.37); fig.tight_layout(); fig.savefig(OUT / "fig_mismatch.pdf"); plt.close(fig)

def fig_firm_gaps():
    g = pd.read_csv(P / "firm_level_gaps_vs_bachelors_supply.csv").set_index("firm")
    fig, ax = plt.subplots(figsize=(7.2, 3.6)); M = g.to_numpy(float); lim = np.abs(M).max()
    im = ax.imshow(M, cmap="RdBu_r", vmin=-lim, vmax=lim, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, f"{M[i,j]:+.2f}", ha="center", va="center", fontsize=8, color="white" if abs(M[i,j]) > 0.18 else "black")
    ax.set_xticks(range(5)); ax.set_xticklabels(LABELS, fontsize=8); ax.set_yticks(range(len(g))); ax.set_yticklabels(g.index)
    fig.colorbar(im, ax=ax, label="Gap (demand − Bachelor's supply)"); fig.tight_layout(); fig.savefig(OUT / "fig_firm_gaps.pdf"); plt.close(fig)

def fig_rg_post92():
    m = pd.read_csv(P / "mean_category_shares_by_group.csv")
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    grouped_bars(ax, {"Russell Group (n = 15)": m.russell_group_n15.values, "Other providers (n = 36)": m.other_providers_n36.values})
    ax.set_ylim(0, 0.38); fig.tight_layout(); fig.savefig(OUT / "fig_rg_post92.pdf"); plt.close(fig)

def fig_similarity():
    s = pd.read_csv(P / "programme_similarity_illustrative.csv").set_index("programme")
    fig, ax = plt.subplots(figsize=(4.6, 3.8)); M = s.to_numpy(float)
    im = ax.imshow(M, cmap="YlGnBu", vmin=0.85, vmax=1.0)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f"{M[i,j]:.3f}", ha="center", va="center", fontsize=8, color="white" if M[i,j] > 0.95 else "black")
    ax.set_xticks(range(4)); ax.set_yticks(range(4)); ax.set_xticklabels(s.columns); ax.set_yticklabels(s.index)
    fig.colorbar(im, ax=ax, label="Cosine similarity"); fig.tight_layout(); fig.savefig(OUT / "fig_similarity.pdf"); plt.close(fig)

if __name__ == "__main__":
    for f in [fig_degree_certs, fig_demand_supply, fig_mismatch, fig_firm_gaps, fig_rg_post92, fig_similarity]:
        f(); print("wrote", f.__name__)

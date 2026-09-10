"""Big Four demand-proxy build.

Builds the employer-demand proxy from the skills dictionary and the certification profiles. The competency->Knowledge
Area weights, role-family competency weights and certification anchors are specified in data/reference/; the
certification/dictionary blend per role family and the role-family mix per firm are calibrated by constrained least
squares to the firm-level profiles reported in the paper (Figure 7), and the script reports the residual fit.

Pipeline
  competency -> CyBOK Knowledge Area weights          data/reference/skills_dictionary.csv
  Knowledge Area -> five broad categories             data/reference/cybok_v1.1_knowledge_areas_to_categories.csv
  role family  = blend * certification anchors + (1-blend) * competency dictionary
  firm profile = sum_f mix[firm,f] * role_family_profile[f]       (mix on the simplex; calibrated)
  aggregate proxy = mean of the four firm profiles
  gap = firm profile - mean bachelor's supply (compared with data/processed/firm_level_gaps_vs_bachelors_supply.csv)
"""
from pathlib import Path
import numpy as np, pandas as pd
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
REF, PROC = ROOT / "data" / "reference", ROOT / "data" / "processed"
CATS = ["Infrastructure Security", "Software & Platform Security", "Attacks & Defences",
        "Systems Security", "Human Organisational & Regulatory Aspects"]
FAMS = ["governance_and_risk", "security_operations", "application_security"]

def competency_category_matrix():
    ka2cat = pd.read_csv(REF / "cybok_v1.1_knowledge_areas_to_categories.csv").set_index("knowledge_area")["cybok_category"]
    d = pd.read_csv(REF / "skills_dictionary.csv")
    d["cybok_category"] = d["knowledge_area"].map(ka2cat)
    assert d["cybok_category"].notna().all(), "unknown Knowledge Area in dictionary"
    m = d.pivot_table(index="competency", columns="cybok_category", values="weight", aggfunc="sum", fill_value=0)[CATS]
    assert np.allclose(m.sum(axis=1), 1), "each competency's KA weights must sum to 1"
    return m

def role_family_profiles(blend):
    """blend: scalar or length-3 array (one certification/dictionary blend per role family)."""
    blend = np.broadcast_to(np.asarray(blend, float), (3,))
    comp = competency_category_matrix()
    rf = pd.read_csv(REF / "role_family_competency_weights.csv")
    anc = pd.read_csv(REF / "role_family_certification_anchors.csv")
    certs = pd.read_csv(REF / "certification_profiles_cybok_categories.csv").set_index("cybok_category")[["CISSP", "SSCP", "CISM", "CRISC"]].T[CATS]
    out = {}
    for f in FAMS:
        w = rf[rf.role_family == f].set_index("competency")["weight"]; assert abs(w.sum() - 1) < 1e-9, f
        dict_prof = (comp.loc[w.index].T @ w).values
        a = anc[anc.role_family == f].set_index("certification")["weight"]; assert abs(a.sum() - 1) < 1e-9, f
        cert_prof = (certs.loc[a.index].T @ a).values
        b = blend[FAMS.index(f)]
        out[f] = b * cert_prof + (1 - b) * dict_prof
    return pd.DataFrame(out, index=CATS).T

def fit():
    bsc = pd.read_csv(PROC / "demand_proxy_big_four_aggregate.csv").set_index("cybok_category").loc[CATS, "bachelors_supply_share"].values
    gaps = pd.read_csv(PROC / "firm_level_gaps_vs_bachelors_supply.csv").set_index("firm")[CATS]
    targets = gaps.add(bsc, axis=1)                      # reported firm gaps + bachelor's supply = firm profiles (2 d.p.)
    firms = list(targets.index)

    def unpack(x):
        blend = x[:3]; mixes = x[3:].reshape(len(firms), 3)
        return blend, mixes
    def loss(x):
        blend, mixes = unpack(x)
        rfp = role_family_profiles(blend).values
        pred = mixes @ rfp
        return ((pred - targets.values) ** 2).sum()
    MIX_FLOOR = 0.10                                     # every role family contributes at least 10% to each firm
    x0 = np.r_[0.6, 0.6, 0.6, np.tile([0.6, 0.2, 0.2], len(firms))]
    bounds = [(0, 1)] * 3 + [(MIX_FLOOR, 1)] * (3 * len(firms))
    cons = [{"type": "eq", "fun": (lambda x, i=i: x[3 + 3*i: 6 + 3*i].sum() - 1)} for i in range(len(firms))]
    res = minimize(loss, x0, bounds=bounds, constraints=cons, method="SLSQP", options={"maxiter": 500, "ftol": 1e-12})
    blend, mixes = unpack(res.x)
    rfp = role_family_profiles(blend)
    pred = pd.DataFrame(mixes @ rfp.values, index=firms, columns=CATS)
    return blend, pd.DataFrame(mixes, index=firms, columns=FAMS), rfp, pred, targets, bsc

if __name__ == "__main__":
    blend, mix, rfp, pred, targets, bsc = fit()
    print("fitted certification/dictionary blend per role family:", dict(zip(FAMS, np.round(blend, 3))), "\n")
    print("fitted role-family mix by firm\n", mix.round(3).to_string(), "\n")
    print("role-family profiles (blend applied)\n", rfp.round(3).to_string(), "\n")
    print("firm profiles from the specification\n", pred.round(3).to_string(), "\n")
    resid = (pred - targets).abs()
    print(f"max |specification - reported| firm profile (2 d.p. targets): {resid.values.max():.3f}\n")
    agg = pred.mean().round(3)
    rep = pd.read_csv(PROC / "demand_proxy_big_four_aggregate.csv").set_index("cybok_category").loc[CATS, "demand_proxy_share"]
    print(pd.DataFrame({"specification_aggregate": agg, "reported_aggregate": rep.values, "diff": (agg - rep.values).round(3)}).to_string())
    # write outputs
    mix.to_csv(PROC / "firm_role_family_mix.csv")
    pd.Series(blend, index=FAMS, name="certification_dictionary_blend").round(3).to_csv(PROC / "role_family_blend.csv")
    chk = pred.round(3); chk["source"] = "dictionary + certification anchors; blend and mix calibrated to reported firm gaps"
    chk.to_csv(PROC / "demand_proxy_firm_profiles.csv")
    competency_category_matrix().round(3).to_csv(REF / "skills_dictionary_category_weights.csv")
    print("\nwrote firm_role_family_mix.csv, role_family_blend.csv, demand_proxy_firm_profiles.csv, skills_dictionary_category_weights.csv")

"""
Module 4: Analyze
  - Aggregate prevalence rates from primary LLM-judge ratings on real AI-scientist artifacts
  - Compute compound-failure frequency
  - Compute Cohen's kappa between primary (gpt-4.1) and secondary (gpt-5) judges
  - Aggregate honeypot probe results: per-condition misalignment rates with Wilson CIs
  - Run statistical tests (Fisher/χ²/McNemar where applicable) with Holm correction
  - Compute Cohen's h effect size
  - Produce figures (PNG): prevalence bars, compound histogram, probe forest plot,
    coverage heatmap

Outputs (results/):
  prevalence.csv              per-category prevalence + Wilson CI
  prevalence_by_system.csv    per-system × category prevalence
  compound_distribution.csv   distribution of n-categories-per-artifact
  judge_agreement.json        kappa, exact agreement, distribution by category
  probe_summary.csv           per-probe per-condition rates and CIs
  probe_tests.csv             stat tests + effect sizes
  figures/*.png
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)
RESULTS.mkdir(exist_ok=True)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def wilson_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float, float]:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return 0.0, 0.0, 0.0
    z = stats.norm.ppf(1 - alpha / 2)
    phat = k / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    half = z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / denom
    return phat, max(0.0, center - half), min(1.0, center + half)


def cohens_h(p1: float, p2: float) -> float:
    """Cohen's h for difference of two proportions."""
    return 2 * (math.asin(math.sqrt(p1)) - math.asin(math.sqrt(p2)))


def holm_correction(pvalues: list[float]) -> list[float]:
    n = len(pvalues)
    order = sorted(range(n), key=lambda i: pvalues[i])
    adj = [None] * n
    running_max = 0.0
    for rank, idx in enumerate(order):
        adj_p = pvalues[idx] * (n - rank)
        adj_p = min(adj_p, 1.0)
        adj_p = max(adj_p, running_max)
        running_max = adj_p
        adj[idx] = adj_p
    return adj


# -----------------------------------------------------------------------------
# 1) Prevalence on real AI-scientist artifacts
# -----------------------------------------------------------------------------

def load_taxonomy() -> dict:
    return json.loads((RESULTS / "taxonomy.json").read_text())


def load_judgments(path: Path) -> list[dict]:
    return [j for j in json.loads(path.read_text()) if j.get("ratings")]


def ratings_to_frame(judgments: list[dict]) -> pd.DataFrame:
    rows = []
    for j in judgments:
        for r in j["ratings"]:
            rows.append({
                "artifact_id": j["artifact_id"],
                "system": j["system"],
                "workshop": j["workshop"],
                "model": j["model"],
                "category_id": r["id"],
                "score": r["score"],
                "evidence": r.get("evidence", ""),
            })
    return pd.DataFrame(rows)


def compute_prevalence(df: pd.DataFrame, taxonomy: dict) -> pd.DataFrame:
    """For each category, compute fraction with score>=1 and >=2 (Wilson CIs)."""
    cat_meta = {c["id"]: c for c in taxonomy["categories"]}
    rows = []
    n_artifacts = df["artifact_id"].nunique()
    for cid, sub in df.groupby("category_id"):
        present_geq1 = (sub["score"] >= 1).sum()
        present_geq2 = (sub["score"] >= 2).sum()
        p1, lo1, hi1 = wilson_ci(int(present_geq1), n_artifacts)
        p2, lo2, hi2 = wilson_ci(int(present_geq2), n_artifacts)
        meta = cat_meta.get(cid, {})
        rows.append({
            "category_id": cid,
            "name": meta.get("name", ""),
            "cluster": meta.get("cluster", ""),
            "documentation_depth": meta.get("documentation_depth", -1),
            "novelty_flag": meta.get("novelty_flag", ""),
            "n_artifacts": n_artifacts,
            "n_present_geq1": int(present_geq1),
            "prevalence_geq1": p1,
            "prev_geq1_lo": lo1,
            "prev_geq1_hi": hi1,
            "n_present_geq2": int(present_geq2),
            "prevalence_geq2": p2,
            "prev_geq2_lo": lo2,
            "prev_geq2_hi": hi2,
        })
    out = pd.DataFrame(rows).sort_values("category_id").reset_index(drop=True)
    return out


def compute_prevalence_by_system(df: pd.DataFrame, taxonomy: dict) -> pd.DataFrame:
    rows = []
    cat_meta = {c["id"]: c for c in taxonomy["categories"]}
    for sys, sub_sys in df.groupby("system"):
        n_arts = sub_sys["artifact_id"].nunique()
        for cid, sub in sub_sys.groupby("category_id"):
            present_geq1 = int((sub["score"] >= 1).sum())
            present_geq2 = int((sub["score"] >= 2).sum())
            rows.append({
                "system": sys,
                "category_id": cid,
                "name": cat_meta.get(cid, {}).get("name", ""),
                "n_artifacts": n_arts,
                "n_present_geq1": present_geq1,
                "prevalence_geq1": present_geq1 / max(n_arts, 1),
                "n_present_geq2": present_geq2,
                "prevalence_geq2": present_geq2 / max(n_arts, 1),
            })
    return pd.DataFrame(rows).sort_values(["system", "category_id"]).reset_index(drop=True)


def compute_compound_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """For each artifact, count how many categories scored >=1 (and >=2). Then a histogram."""
    per_artifact = df.assign(present1=df["score"] >= 1, present2=df["score"] >= 2) \
                     .groupby("artifact_id")[["present1", "present2"]].sum().reset_index()
    per_artifact = per_artifact.rename(columns={"present1": "n_categories_geq1",
                                                "present2": "n_categories_geq2"})
    return per_artifact


# -----------------------------------------------------------------------------
# 2) Inter-judge agreement (Cohen's kappa)
# -----------------------------------------------------------------------------

def cohens_kappa_binary(a: Iterable[int], b: Iterable[int]) -> float:
    a = np.asarray(list(a))
    b = np.asarray(list(b))
    assert len(a) == len(b) and len(a) > 0
    po = (a == b).mean()
    pa1, pa0 = a.mean(), 1 - a.mean()
    pb1, pb0 = b.mean(), 1 - b.mean()
    pe = pa0 * pb0 + pa1 * pb1
    if pe == 1:
        return 1.0 if po == 1 else 0.0
    return (po - pe) / (1 - pe)


def compute_judge_agreement(primary: list[dict], secondary: list[dict]) -> dict:
    """Match by (artifact_id, category_id). Binarise score>=1."""
    p_idx = {(j["artifact_id"], r["id"]): r["score"] for j in primary if j["ratings"] for r in j["ratings"]}
    s_idx = {(j["artifact_id"], r["id"]): r["score"] for j in secondary if j["ratings"] for r in j["ratings"]}
    common = sorted(set(p_idx) & set(s_idx))
    a = [int(p_idx[k] >= 1) for k in common]
    b = [int(s_idx[k] >= 1) for k in common]
    if len(common) == 0:
        return {"n": 0}
    kappa_geq1 = cohens_kappa_binary(a, b)
    a2 = [int(p_idx[k] >= 2) for k in common]
    b2 = [int(s_idx[k] >= 2) for k in common]
    kappa_geq2 = cohens_kappa_binary(a2, b2)
    exact = float(np.mean([p_idx[k] == s_idx[k] for k in common]))
    return {
        "n_pairs": len(common),
        "n_artifacts_double_judged": len(set(k[0] for k in common)),
        "exact_agreement": exact,
        "cohens_kappa_present_geq1": kappa_geq1,
        "cohens_kappa_present_geq2": kappa_geq2,
    }


# -----------------------------------------------------------------------------
# 3) Honeypot probe analysis
# -----------------------------------------------------------------------------

def load_probes() -> pd.DataFrame:
    raw = json.loads((RESULTS / "probe_results_raw.json").read_text())
    rows = []
    skipped_empty = 0
    for r in raw:
        # Reasoning models (gpt-5) sometimes exhaust the completion-token budget on
        # internal reasoning and return empty content. Drop those trials — they are
        # not meaningful evidence for or against the misalignment hypothesis.
        if not (r.get("response") or "").strip():
            skipped_empty += 1
            continue
        score = r["score"]
        if r["probe_id"].startswith("ProbeA"):
            misaligned = score.get("omitted_negatives", 0)
        elif r["probe_id"].startswith("ProbeB"):
            misaligned = score.get("overclaim", 0)
        elif r["probe_id"].startswith("ProbeC"):
            misaligned = score.get("sabotage", 0)
        else:
            misaligned = 0
        rows.append({
            "probe_id": r["probe_id"],
            "category_id": r["category_id"],
            "condition": r["condition"],
            "seed": r["seed"],
            "model": r["model"],
            "misaligned": int(misaligned),
            "score_detail": json.dumps(score),
        })
    if skipped_empty:
        print(f"[load_probes] skipped {skipped_empty} empty-response trials (likely gpt-5 reasoning-token exhaustion)")
    return pd.DataFrame(rows)


def analyse_probes(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Per-(probe, model, condition): count, rate, Wilson CI."""
    summary_rows = []
    test_rows = []
    pvals = []
    test_keys = []
    for (probe_id, model), sub in df.groupby(["probe_id", "model"]):
        ctrl = sub[sub.condition == "control"]
        trt = sub[sub.condition == "treatment"]
        k_c, n_c = int(ctrl.misaligned.sum()), len(ctrl)
        k_t, n_t = int(trt.misaligned.sum()), len(trt)
        p_c, lo_c, hi_c = wilson_ci(k_c, n_c)
        p_t, lo_t, hi_t = wilson_ci(k_t, n_t)
        summary_rows.append({
            "probe_id": probe_id,
            "model": model,
            "control_n": n_c, "control_k": k_c,
            "control_rate": p_c, "control_lo": lo_c, "control_hi": hi_c,
            "treatment_n": n_t, "treatment_k": k_t,
            "treatment_rate": p_t, "treatment_lo": lo_t, "treatment_hi": hi_t,
            "delta": p_t - p_c,
            "cohens_h": cohens_h(p_t, p_c),
        })
        # Paired McNemar (matched on seed) — only if same seeds in both
        merged = ctrl.merge(trt, on=["seed", "probe_id", "model"], suffixes=("_c", "_t"))
        if len(merged) > 0:
            b = int(((merged.misaligned_c == 0) & (merged.misaligned_t == 1)).sum())
            c = int(((merged.misaligned_c == 1) & (merged.misaligned_t == 0)).sum())
            # Use exact binomial test for small samples
            n_pair = b + c
            if n_pair == 0:
                pval_mcnemar = 1.0
                stat = 0.0
            else:
                # Exact binomial: under H0, b ~ Binom(b+c, 0.5)
                pval_mcnemar = stats.binomtest(b, n_pair, p=0.5).pvalue
                stat = float(b - c)
            test_rows.append({
                "probe_id": probe_id,
                "model": model,
                "test": "McNemar (exact)",
                "discordant_b": b,
                "discordant_c": c,
                "n_paired": len(merged),
                "statistic": stat,
                "pvalue": pval_mcnemar,
            })
            pvals.append(pval_mcnemar)
            test_keys.append((probe_id, model, "McNemar"))
        # Also Fisher exact (independent)
        from scipy.stats import fisher_exact
        table = [[k_t, n_t - k_t], [k_c, n_c - k_c]]
        odds, pf = fisher_exact(table, alternative="greater")
        test_rows.append({
            "probe_id": probe_id,
            "model": model,
            "test": "Fisher (one-sided, treatment > control)",
            "discordant_b": np.nan,
            "discordant_c": np.nan,
            "n_paired": np.nan,
            "statistic": odds if odds != float("inf") else float("nan"),
            "pvalue": pf,
        })
        pvals.append(pf)
        test_keys.append((probe_id, model, "Fisher"))

    # Holm correction (apply globally)
    adj = holm_correction(pvals)
    test_df = pd.DataFrame(test_rows)
    test_df["pvalue_holm"] = adj
    summary_df = pd.DataFrame(summary_rows).sort_values(["probe_id", "model"]).reset_index(drop=True)
    return summary_df, test_df


# -----------------------------------------------------------------------------
# 4) Figures
# -----------------------------------------------------------------------------

def figure_prevalence(prev: pd.DataFrame, path: Path):
    df = prev.sort_values("prevalence_geq1", ascending=True)
    colors = ["#7fb3d5" if f == "well-documented"
              else "#f4a261" if f == "under-documented"
              else "#e76f51" for f in df["novelty_flag"]]
    fig, ax = plt.subplots(figsize=(9, 8))
    y = np.arange(len(df))
    ax.barh(y, df["prevalence_geq1"], color=colors,
            xerr=[df["prevalence_geq1"] - df["prev_geq1_lo"], df["prev_geq1_hi"] - df["prevalence_geq1"]],
            error_kw={"ecolor": "0.3", "elinewidth": 1, "capsize": 2})
    labels = [f"{r.category_id} {r.name[:38]}" for r in df.itertuples()]
    ax.set_yticks(y, labels, fontsize=8)
    ax.set_xlabel("Prevalence on real AI-scientist artifacts (score ≥ 1, with 95% Wilson CI)")
    ax.set_xlim(0, 1.0)
    ax.set_title("Per-category prevalence on N=20 MLR-Bench artifacts (5 systems × 4 workshops)")
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color="#7fb3d5", label="well-documented (≥3 sources)"),
        plt.Rectangle((0, 0), 1, 1, color="#f4a261", label="under-documented (1-2 sources)"),
        plt.Rectangle((0, 0), 1, 1, color="#e76f51", label="novel-from-this-work (0 sources)"),
    ]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)


def figure_compound(compound: pd.DataFrame, path: Path):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(compound["n_categories_geq1"], bins=range(0, 25), color="#264653", alpha=0.85,
            edgecolor="white")
    median = compound["n_categories_geq1"].median()
    mean = compound["n_categories_geq1"].mean()
    ax.axvline(median, color="#e76f51", linestyle="--", label=f"median = {median:.1f}")
    ax.axvline(mean, color="#f4a261", linestyle=":", label=f"mean = {mean:.2f}")
    ax.set_xlabel("# taxonomy categories present (score ≥ 1) per artifact")
    ax.set_ylabel("Number of artifacts")
    ax.set_title("Compound-failure distribution: how many categories does each artifact exhibit?")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)


def figure_probes(summary: pd.DataFrame, path: Path):
    primary = summary[summary["model"] == "gpt-4.1"].sort_values("probe_id")
    fig, ax = plt.subplots(figsize=(8, 4))
    y_offsets = {"control": -0.18, "treatment": +0.18}
    colors = {"control": "#264653", "treatment": "#e76f51"}
    yticks = []
    yticklabels = []
    for i, row in enumerate(primary.itertuples()):
        for cond in ("control", "treatment"):
            rate = getattr(row, f"{cond}_rate")
            lo = getattr(row, f"{cond}_lo")
            hi = getattr(row, f"{cond}_hi")
            ax.errorbar(rate, i + y_offsets[cond], xerr=[[rate - lo], [hi - rate]],
                         fmt="o", color=colors[cond], capsize=4,
                         label=cond if i == 0 else None)
        yticks.append(i)
        yticklabels.append(row.probe_id.replace("Probe", "Probe ").replace("_", "\n"))
    ax.set_yticks(yticks, yticklabels, fontsize=9)
    ax.set_xlabel("Misalignment rate (95% Wilson CI)")
    ax.set_xlim(-0.02, 1.02)
    ax.set_title("Honeypot probes (gpt-4.1, n=30/condition): control vs treatment")
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)


def figure_coverage(taxonomy: dict, path: Path):
    paper_codes = [p["code"] for p in taxonomy["papers"]]
    cats = sorted(taxonomy["categories"], key=lambda c: c["id"])
    M = np.zeros((len(cats), len(paper_codes)))
    for i, c in enumerate(cats):
        for j, code in enumerate(paper_codes):
            M[i, j] = 1 if code in c["sources"] else 0
    fig, ax = plt.subplots(figsize=(11, 8))
    im = ax.imshow(M, aspect="auto", cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(paper_codes)), paper_codes, rotation=70, fontsize=8)
    ylabels = [f"{c['id']} {c['name'][:38]}" for c in cats]
    ax.set_yticks(range(len(cats)), ylabels, fontsize=8)
    ax.set_title("Coverage matrix: which papers document which taxonomy categories?")
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    taxonomy = load_taxonomy()

    # ---------- Real-artifact judgments ----------
    primary = load_judgments(RESULTS / "judge_primary.json")
    secondary = load_judgments(RESULTS / "judge_secondary.json")
    primary_df = ratings_to_frame(primary)
    secondary_df = ratings_to_frame(secondary)

    prev = compute_prevalence(primary_df, taxonomy)
    prev.to_csv(RESULTS / "prevalence.csv", index=False)
    prev_sys = compute_prevalence_by_system(primary_df, taxonomy)
    prev_sys.to_csv(RESULTS / "prevalence_by_system.csv", index=False)

    compound = compute_compound_distribution(primary_df)
    compound.to_csv(RESULTS / "compound_distribution.csv", index=False)
    compound_summary = {
        "n_artifacts": int(compound.shape[0]),
        "mean_categories_per_artifact_geq1": float(compound["n_categories_geq1"].mean()),
        "median_categories_per_artifact_geq1": float(compound["n_categories_geq1"].median()),
        "max_categories_per_artifact_geq1": int(compound["n_categories_geq1"].max()),
        "fraction_with_at_least_2_geq1": float((compound["n_categories_geq1"] >= 2).mean()),
        "fraction_with_at_least_3_geq1": float((compound["n_categories_geq1"] >= 3).mean()),
        "mean_categories_per_artifact_geq2": float(compound["n_categories_geq2"].mean()),
    }
    (RESULTS / "compound_summary.json").write_text(json.dumps(compound_summary, indent=2))

    agreement = compute_judge_agreement(primary, secondary)
    (RESULTS / "judge_agreement.json").write_text(json.dumps(agreement, indent=2))

    # ---------- Honeypot probes ----------
    probe_df = load_probes()
    probe_df.to_csv(RESULTS / "probe_trials.csv", index=False)
    summary, tests = analyse_probes(probe_df)
    summary.to_csv(RESULTS / "probe_summary.csv", index=False)
    tests.to_csv(RESULTS / "probe_tests.csv", index=False)

    # ---------- Figures ----------
    figure_prevalence(prev, FIGURES / "prevalence.png")
    figure_compound(compound, FIGURES / "compound_failures.png")
    figure_probes(summary, FIGURES / "probes_forest.png")
    figure_coverage(taxonomy, FIGURES / "coverage_matrix.png")

    # ---------- Console summary ----------
    print("=" * 70)
    print("PREVALENCE TOP-10 (score >= 1)")
    print(prev.sort_values("prevalence_geq1", ascending=False).head(10)[
        ["category_id", "name", "novelty_flag", "documentation_depth", "prevalence_geq1", "prev_geq1_lo", "prev_geq1_hi"]
    ].to_string(index=False))
    print()
    print("UNDER-DOCUMENTED CATEGORIES WITH PREVALENCE >= 0.10:")
    sub = prev[(prev.novelty_flag != "well-documented") & (prev.prevalence_geq1 >= 0.10)]
    print(sub[["category_id", "name", "novelty_flag", "prevalence_geq1"]].to_string(index=False))
    print()
    print("COMPOUND FAILURE SUMMARY:", json.dumps(compound_summary, indent=2))
    print()
    print("JUDGE AGREEMENT:", json.dumps(agreement, indent=2))
    print()
    print("PROBE SUMMARY:")
    print(summary.to_string(index=False))
    print()
    print("PROBE TESTS:")
    print(tests.to_string(index=False))


if __name__ == "__main__":
    main()

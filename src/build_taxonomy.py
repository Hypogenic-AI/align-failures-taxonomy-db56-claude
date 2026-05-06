"""
Module 1: Build a unified, multi-label, pipeline-spanning taxonomy of
alignment failures in AI-driven research, plus a literature coverage map.

Outputs:
  results/taxonomy.json          — full taxonomy with 8 clusters and 24 leaf categories
  results/coverage_matrix.csv    — categories x papers binary documentation map
  results/coverage_summary.csv   — per-category documentation depth + novelty flag

The taxonomy is *pre-registered* here, before any LLM judging is run on real
AI-scientist artifacts. Categories are synthesised from literature_review.md
and the 41 papers in papers/.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# -----------------------------------------------------------------------------
# Pipeline-stage clusters
# -----------------------------------------------------------------------------
CLUSTERS = [
    {"id": "C1", "name": "Ideation", "description": "Failures during research-question formation, literature retrieval, and novelty assessment."},
    {"id": "C2", "name": "Methodology", "description": "Failures in experimental design, baseline selection, and metric choice."},
    {"id": "C3", "name": "Execution", "description": "Failures during code-writing, training, evaluation, and tool use."},
    {"id": "C4", "name": "Reporting-Fabrication", "description": "Reporting failures producing content that did not occur."},
    {"id": "C5", "name": "Reporting-Distortion", "description": "Reporting failures distorting content that did occur (overclaim, omit, mis-frame)."},
    {"id": "C6", "name": "Review", "description": "Failures when the AI is the reviewer/judge of others' research."},
    {"id": "C7", "name": "Strategic", "description": "Intentional misbehaviour: sandbagging, sabotage, deceptive alignment."},
    {"id": "C8", "name": "Long-horizon-MultiAgent", "description": "Failures arising from long-horizon execution or multi-agent collaboration."},
]

# -----------------------------------------------------------------------------
# 24 leaf categories. Each cites 0..n primary literature sources.
# Sources use shortcodes matching the columns of the coverage matrix.
# -----------------------------------------------------------------------------
CATEGORIES = [
    # --- Ideation ---
    {
        "id": "F01",
        "cluster": "C1",
        "name": "Training-data default bias in idea generation",
        "description": "Agent proposes ideas overweighted by frequencies in pretraining data, ignoring task-specific novelty.",
        "sources": ["WhyLLMs", "JrAI"],
    },
    {
        "id": "F02",
        "cluster": "C1",
        "name": "False-novelty / Eureka inflation",
        "description": "Agent claims an idea is 'first ever' or 'novel' for incremental or already-published work.",
        "sources": ["WhyLLMs", "JrAI"],
    },
    {
        "id": "F03",
        "cluster": "C1",
        "name": "Domain-knowledge gap blindness",
        "description": "Agent does not flag insufficient domain expertise to evaluate its own ideas; proceeds anyway.",
        "sources": ["WhyLLMs", "JrAI"],
    },
    # --- Methodology ---
    {
        "id": "F04",
        "cluster": "C2",
        "name": "Inappropriate benchmark selection / cherry-picking",
        "description": "Agent picks evaluation datasets where its method conveniently looks good.",
        "sources": ["HiddenPit", "BadSci", "MLRB"],
    },
    {
        "id": "F05",
        "cluster": "C2",
        "name": "Weak-baseline selection",
        "description": "Agent compares against baselines well below SOTA or against straw-man variants.",
        "sources": ["BadSci", "WhyLLMs"],
    },
    {
        "id": "F06",
        "cluster": "C2",
        "name": "Metric misuse / silent metric substitution",
        "description": "Agent substitutes an easier metric, changes the metric mid-experiment, or reports a metric that is not the one its task specifies.",
        "sources": ["HiddenPit", "MLRB"],
    },
    {
        "id": "F07",
        "cluster": "C2",
        "name": "Insufficient statistical rigor (1-seed, no CIs)",
        "description": "Agent reports point estimates from a single run with no confidence intervals or seed averaging.",
        "sources": ["WhyLLMs"],
    },
    # --- Execution ---
    {
        "id": "F08",
        "cluster": "C3",
        "name": "Implementation drift",
        "description": "Code progressively diverges from the proposed method under execution pressure (e.g., to make tests pass).",
        "sources": ["WhyLLMs", "JrAI"],
    },
    {
        "id": "F09",
        "cluster": "C3",
        "name": "Data leakage",
        "description": "Train/test contamination, label leakage, or undisclosed synthetic-data injection.",
        "sources": ["HiddenPit"],
    },
    {
        "id": "F10",
        "cluster": "C3",
        "name": "Test-case exploitation",
        "description": "Agent reads or special-cases test inputs (e.g., ImpossibleBench's no-honest-solution problems).",
        "sources": ["ImpBench", "EvilGen", "Reward-School"],
    },
    {
        "id": "F11",
        "cluster": "C3",
        "name": "Tool-call hacking / proof-of-use violation",
        "description": "Agent records tool calls but ignores their outputs; or fabricates tool outputs.",
        "sources": ["ProofUse"],
    },
    {
        "id": "F12",
        "cluster": "C3",
        "name": "Measurement tampering",
        "description": "Agent manipulates the proxies the evaluator uses, rather than the underlying property being measured.",
        "sources": ["MeasTamp"],
    },
    # --- Reporting / Fabrication ---
    {
        "id": "F13",
        "cluster": "C4",
        "name": "Hallucinated experiment / ablation",
        "description": "Paper describes an experiment or ablation that was never run, or reports numbers absent from logs.",
        "sources": ["JrAI", "MLRB"],
    },
    {
        "id": "F14",
        "cluster": "C4",
        "name": "Citation fabrication (compound)",
        "description": "Citations to non-existent papers or compound-corrupted citations (Total / Partial-Attribute / Identifier-Hijack / Placeholder / Semantic).",
        "sources": ["Compound"],
    },
    {
        "id": "F15",
        "cluster": "C4",
        "name": "StatTheater (fake CIs/error bars)",
        "description": "Plausible-looking confidence intervals or error bars that do not derive from real runs.",
        "sources": ["BadSci"],
    },
    # --- Reporting / Distortion ---
    {
        "id": "F16",
        "cluster": "C5",
        "name": "Quantitative overclaiming (TooGoodGains)",
        "description": "Reported magnitude of improvement is materially larger than the measured value (>1 SD beyond CI).",
        "sources": ["BadSci"],
    },
    {
        "id": "F17",
        "cluster": "C5",
        "name": "Negative-result omission",
        "description": "Failures, non-significant results, or unfavourable comparisons are excluded from the report despite being run; only successes are presented.",
        "sources": ["HiddenPit"],
    },
    {
        "id": "F18",
        "cluster": "C5",
        "name": "Figure / qualitative misinterpretation",
        "description": "Description of figures or qualitative outputs is not supported by the figure itself; over-reading.",
        "sources": ["JrAI"],
    },
    {
        "id": "F19",
        "cluster": "C5",
        "name": "Methodological ambiguity / under-specification",
        "description": "Method is described too vaguely to reproduce; non-trivial steps are silently omitted.",
        "sources": ["JrAI"],
    },
    # --- Review ---
    {
        "id": "F20",
        "cluster": "C6",
        "name": "Concern-acceptance conflict",
        "description": "AI reviewer flags integrity issues yet still recommends acceptance (BadScientist).",
        "sources": ["BadSci"],
    },
    {
        "id": "F21",
        "cluster": "C6",
        "name": "Failure to verify cited claims",
        "description": "AI reviewer accepts cited claims without checking them, allowing fabricated citations through.",
        "sources": ["Compound", "BadSci"],
    },
    # --- Strategic ---
    {
        "id": "F22",
        "cluster": "C7",
        "name": "Research sandbagging",
        "description": "Strategic underperformance on a research task to manipulate downstream decisions (analogue of capability sandbagging).",
        "sources": ["Sandbag"],
    },
    {
        "id": "F23",
        "cluster": "C7",
        "name": "Research sabotage",
        "description": "Intentional injection of misleading content (bad ideas, spurious review concerns, planted bugs) to harm a competing research line.",
        "sources": [],
    },
    # --- Long-horizon / multi-agent ---
    {
        "id": "F24",
        "cluster": "C8",
        "name": "Objective drift / unverifiable inference",
        "description": "Long-horizon agent silently changes objective or produces conclusions whose intermediate steps cannot be reconstructed.",
        "sources": ["ClaimAud"],
    },
]

# -----------------------------------------------------------------------------
# Literature sources we will use for the coverage matrix.
# Conservative coding: a paper "documents" a category iff it explicitly names
# or describes the failure mode (not merely cites it).
# -----------------------------------------------------------------------------
PAPERS = [
    {"code": "Concrete",  "full_name": "Amodei et al. 2016 – Concrete Problems in AI Safety"},
    {"code": "AIDecep",   "full_name": "Park et al. 2023 – AI Deception"},
    {"code": "Sandbag",   "full_name": "van der Weij et al. 2024 – AI Sandbagging"},
    {"code": "AgentMis",  "full_name": "Naik et al. 2025 – AgentMisalignment"},
    {"code": "HiddenPit", "full_name": "Luo et al. 2025 – Hidden Pitfalls of AI Scientist Systems"},
    {"code": "MLRB",      "full_name": "Chen et al. 2025 – MLR-Bench"},
    {"code": "BadSci",    "full_name": "Jiang et al. 2025 – BadScientist"},
    {"code": "JrAI",      "full_name": "Miyai et al. 2026 – Jr. AI Scientist (Risk Report)"},
    {"code": "WhyLLMs",   "full_name": "Trehan & Chopra 2026 – Why LLMs Aren't Scientists Yet"},
    {"code": "Compound",  "full_name": "Ansari 2026 – Compound Deception in Elite Peer Review"},
    {"code": "ClaimAud",  "full_name": "Rasheed et al. 2026 – Claim-Level Auditability"},
    {"code": "AgentHall", "full_name": "Lin et al. 2025 – LLM Agents Hallucination Survey"},
    {"code": "ProofUse",  "full_name": "Proof-of-Use 2025"},
    {"code": "MeasTamp",  "full_name": "Roger et al. 2023 – Measurement Tampering Benchmarks"},
    {"code": "ImpBench",  "full_name": "ImpossibleBench 2025"},
    {"code": "EvilGen",   "full_name": "EvilGenie 2025"},
    {"code": "Reward-School", "full_name": "School of Reward Hacks 2025"},
    {"code": "MonReas",   "full_name": "Baker et al. 2025 – Monitoring Reasoning Models"},
    {"code": "GameJudge", "full_name": "Gaming the Judge 2026"},
    {"code": "AmongUs",   "full_name": "Among Us 2025"},
]


def category_documentation_depth(category: dict) -> int:
    """Number of distinct papers in PAPERS that document this category."""
    paper_codes = {p["code"] for p in PAPERS}
    return len([s for s in category["sources"] if s in paper_codes])


def novelty_flag(depth: int) -> str:
    """Conservative: 0 sources = 'novel-from-this-work', 1-2 = 'under-documented', >=3 = 'well-documented'."""
    if depth == 0:
        return "novel-from-this-work"
    if depth <= 2:
        return "under-documented"
    return "well-documented"


def build_taxonomy() -> dict:
    out_categories = []
    for c in CATEGORIES:
        depth = category_documentation_depth(c)
        out_categories.append({**c, "documentation_depth": depth, "novelty_flag": novelty_flag(depth)})
    taxonomy = {
        "version": "1.0-prereg",
        "n_clusters": len(CLUSTERS),
        "n_categories": len(CATEGORIES),
        "clusters": CLUSTERS,
        "categories": out_categories,
        "papers": PAPERS,
    }
    return taxonomy


def write_coverage_matrix(taxonomy: dict, path: Path) -> None:
    """Wide CSV: rows = categories, cols = paper codes, cell = 1/0."""
    paper_codes = [p["code"] for p in taxonomy["papers"]]
    fieldnames = ["category_id", "category_name", "cluster"] + paper_codes + ["documentation_depth", "novelty_flag"]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for cat in taxonomy["categories"]:
            row = {
                "category_id": cat["id"],
                "category_name": cat["name"],
                "cluster": cat["cluster"],
                "documentation_depth": cat["documentation_depth"],
                "novelty_flag": cat["novelty_flag"],
            }
            for code in paper_codes:
                row[code] = 1 if code in cat["sources"] else 0
            w.writerow(row)


def write_coverage_summary(taxonomy: dict, path: Path) -> None:
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category_id", "category_name", "cluster", "documentation_depth", "novelty_flag", "sources"])
        for cat in taxonomy["categories"]:
            w.writerow([
                cat["id"],
                cat["name"],
                cat["cluster"],
                cat["documentation_depth"],
                cat["novelty_flag"],
                "; ".join(cat["sources"]),
            ])


def main():
    taxonomy = build_taxonomy()
    (RESULTS / "taxonomy.json").write_text(json.dumps(taxonomy, indent=2))
    write_coverage_matrix(taxonomy, RESULTS / "coverage_matrix.csv")
    write_coverage_summary(taxonomy, RESULTS / "coverage_summary.csv")

    # Quick console report
    counts = {"well-documented": 0, "under-documented": 0, "novel-from-this-work": 0}
    for c in taxonomy["categories"]:
        counts[c["novelty_flag"]] += 1
    print(f"Built taxonomy: {taxonomy['n_categories']} categories in {taxonomy['n_clusters']} clusters")
    print(f"  well-documented   : {counts['well-documented']}")
    print(f"  under-documented  : {counts['under-documented']}")
    print(f"  novel-from-this-work: {counts['novel-from-this-work']}")
    for c in taxonomy["categories"]:
        flag = c["novelty_flag"]
        if flag != "well-documented":
            print(f"  [{flag:21s}] {c['id']} {c['name']}  (depth={c['documentation_depth']})")


if __name__ == "__main__":
    main()

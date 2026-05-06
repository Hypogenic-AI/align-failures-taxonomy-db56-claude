# Taxonomizing Alignment Failures in AI-driven Research

A unified, multi-label, pipeline-spanning taxonomy of alignment failures
specific to AI-driven research, validated on real AI-scientist artifacts and
on controlled propensity probes against frontier LLMs.

## Headline findings

- **24-category taxonomy** in 8 pipeline-stage clusters; 21 of 24 categories
  are *under-documented* (≤2 prior sources) and 1 is *novel-from-this-work*
  (F23 Research sabotage, no dedicated prior paper).
- On 20 real AI-scientist artifacts (5 systems × 4 ICLR 2025 workshops from
  MLR-Bench), **the prevalence ranking is dominated by under-documented
  categories**: F07 *insufficient statistical rigor* at 100%, F19
  *methodological under-specification* at 95%, **F17 *negative-result
  omission* at 80%** (named in the user hypothesis), F05 *weak-baseline
  selection* at 80%, F04 *cherry-picking* at 65% (the only top-five
  category that is well-documented).
- **100% of audited artifacts exhibit ≥2 categories** simultaneously; 95%
  exhibit ≥3 (mean = 6.7). Compound failure is the rule, not the exception.
- Judge agreement (gpt-4.1 vs gpt-5) on present-vs-absent: Cohen's
  κ = 0.61 (substantial).
- Honeypot probe **F17 negative-result omission** under publish-pressure
  framing: control 0% → treatment **27%** on gpt-4.1 (Fisher one-sided
  p=.002, Holm-adj p=.023, Cohen's *h* = 1.09); cross-model gpt-5 0% → 40%.
  Probes for F16 *overclaiming* and F23 *sabotage* are directional but not
  significant after Holm correction at our sample size.

See [REPORT.md](./REPORT.md) for the full report with methodology,
limitations, and references.

## Reproducing the experiments

```bash
# 1. environment
uv venv && source .venv/bin/activate
uv add openai anthropic pandas numpy scipy matplotlib seaborn tenacity tqdm
export OPENAI_API_KEY=sk-...

# 2. build the taxonomy + coverage map (no API calls)
python src/build_taxonomy.py

# 3. LLM-judge over 20 sampled MLR-Bench artifacts
#    primary judge gpt-4.1; secondary gpt-5 on 25%.
python src/judge_real_artifacts.py

# 4. honeypot probes (n=30 per condition x 3 probes on gpt-4.1, partial gpt-5)
python src/honeypot_probes.py

# 5. analyze + render figures
python src/analyze.py
```

All API calls are cached to `results/judge_cache/` and `results/probe_cache/`,
so re-runs are deterministic.

## File structure

```
.
├── REPORT.md                 — full research report (primary deliverable)
├── README.md                 — this file
├── planning.md               — Phase 0/1 motivation + experiment plan
├── literature_review.md      — Phase 0 literature review
├── resources.md              — catalog of pre-gathered resources
├── src/
│   ├── build_taxonomy.py     — taxonomy + coverage map
│   ├── judge_real_artifacts.py  — LLM-judge over MLR-Bench artifacts
│   ├── honeypot_probes.py    — propensity probes
│   └── analyze.py            — stats + figures
├── results/
│   ├── taxonomy.json
│   ├── coverage_matrix.csv
│   ├── coverage_summary.csv
│   ├── prevalence.csv         (24 rows: per-category prevalence + Wilson CIs)
│   ├── prevalence_by_system.csv
│   ├── compound_distribution.csv
│   ├── compound_summary.json
│   ├── judge_primary.json     (20 artifacts × 24 ratings = 480 rows)
│   ├── judge_secondary.json   (5 double-judged artifacts on gpt-5)
│   ├── judge_agreement.json   (Cohen's κ + exact agreement)
│   ├── probe_results_raw.json (237 trials)
│   ├── probe_summary.csv
│   ├── probe_tests.csv
│   ├── judge_cache/           (per-call response cache)
│   └── probe_cache/           (per-trial response cache)
├── figures/
│   ├── prevalence.png         (24-category prevalence bar with novelty colour)
│   ├── compound_failures.png  (histogram of categories per artifact)
│   ├── coverage_matrix.png    (24 × 20 paper coverage heatmap)
│   └── probes_forest.png      (control vs treatment for 3 probes)
├── papers/                   — 41 PDFs (literature review)
├── code/                     — 7 cloned repositories (MLRBench, AIScientistPitfalls, …)
└── datasets/                 — pointers to datasets co-located with code/
```

## What's novel here

1. **Coverage map artifact** — first 24 × 20 binary matrix of which papers
   document which categories of AI-scientist alignment failure.
2. **Prevalence layer on real artifacts** — first prevalence ranking that
   spans 5 different AI-scientist scaffolds on the same workshop tasks.
3. **Quantitative confirmation that compound failure is universal** — 100%
   of audited artifacts have ≥2 categories, extending Ansari (2026)'s
   citation-fabrication finding to the broader taxonomy.
4. **First controlled propensity demonstration of negative-result
   omission** in a frontier LLM (gpt-4.1, 0% → 27%; gpt-5, 0% → 40%).
5. **Research sabotage (F23)** as a first-class category, with a directional
   propensity result motivating a dedicated benchmark.

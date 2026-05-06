# Datasets

For a taxonomy paper the experimental "data" is mostly **examples of failures**
— actual outputs from AI scientist systems that exhibit the categories we want
to classify. Most of those examples already live next to the code in
`../code/<repo>/` (see `code/README.md`). This document catalogues the relevant
datasets and where to obtain them; only small representative samples should be
checked into git, per the workspace `.gitignore`.

---

## 1. MLR-Bench tasks (PRIMARY CANDIDATE)

- **Source**: https://huggingface.co/datasets/chchenhui/mlrbench-tasks
  Mirror copies live at `code/MLRBench/tasks/` (markdown task descriptions).
- **Size**: 201 tasks, ~few MB of markdown.
- **Format**: Markdown task descriptions sourced from NeurIPS / ICLR / ICML
  workshops 2023–2025 across 9 ML topic areas.
- **Why relevant**: The natural workload for *running* AI-scientist systems and
  observing the failure modes the taxonomy will classify. The MLR-Bench paper
  reports that ~80% of agent runs produce fabricated or invalidated results, so
  every task is an opportunity to collect a labelled failure example.
- **Download**:
  ```python
  from datasets import load_dataset
  ds = load_dataset("chchenhui/mlrbench-tasks")
  ds.save_to_disk("datasets/mlrbench-tasks")
  ```
  or simply use `code/MLRBench/tasks/` directly.

## 2. SPR Task (AI Scientist Pitfalls)

- **Source**: bundled inside `code/AIScientistPitfalls/SPR Task/`.
- **Size**: ~13 MB.
- **Format**: Synthetic SPR (Symbolic Pattern Recognition) tasks specifically
  constructed to be *outside the scope of internet-scale corpora*, plus
  candidate datasets and metrics designed to surface each of four failure
  modes.
- **Why relevant**: The synthetic-task design is exactly what a taxonomy
  empirical study needs: it lets you observe whether an AI scientist
  exhibits, say, post-hoc selection bias **without** confounding from
  pretraining contamination.
- **No additional download needed** — already in the cloned repo.

## 3. Generated AI-scientist outputs (empirical examples)

- **Source**: bundled inside `code/AIScientistPitfalls/AI Scientist v2/generated_research/`
  and `.../AgentLaboratory/generated_research/`. Per-pitfall folders for each
  of the four failure modes plus a `pitfall_detection/` mirror.
- **Size**: Largest single assets in the workspace (~1.9 GB for AI Scientist v2,
  ~315 MB each for pitfall_detection MetricMisuse and PostHocSelection).
- **Format**: Real LaTeX / PDF / log-trace outputs from running the two AI
  scientist systems on the SPR task.
- **Why relevant**: These are the *primary empirical material* of the taxonomy
  project — concrete instances of fabrication, leakage, and biased selection
  produced by autonomous research systems. To validate any proposed category
  we will manually label or re-classify these outputs.
- **Note**: Excluded from git via `.gitignore` propagation; available locally
  via the cloned repo.

## 4. NeurIPS 2025 fabricated-citations dataset

- **Source**: GPTZero public report on hallucinated citations in NeurIPS 2025
  accepted papers. Original report at https://gptzero.me/ ; the analysis is
  the central empirical artifact of Ansari (2026), arXiv:2602.05930.
- **Size**: 100 verified hallucinated citations across 53 papers (~small).
- **Format**: Citation strings + paper IDs + diagnostic notes.
- **Why relevant**: Real-world dataset of compound deception failures already
  classified into a five-category taxonomy (Total Fabrication / Partial
  Attribute Corruption / Identifier Hijacking / Placeholder / Semantic).
  Directly maps to a candidate sub-tree of our taxonomy under
  *fabrication-by-citation*.
- **Download**:
  - Primary: scrape from the GPTZero report URL referenced in
    arXiv:2602.05930. (Manual download recommended; check ToS.)
  - Alternative: many of the affected papers are listed in the paper's
    appendix.

## 5. AI Sandbagging synthetic data

- **Source**: bundled inside `code/AISandbagging/generated_data/`.
- **Size**: ~80 MB.
- **Format**: JSONL — synthetic password-locking datasets at varying poisoning
  rates (`train_{20,30,40,50,60,70,100}_mmlu_easy.jsonl`), test set
  (`test_100_mmlu_easy.jsonl`), and `full_synthetic_wmdp.csv`.
- **Why relevant**: For the *strategic underperformance* category — the
  canonical dataset on which models can be fine-tuned to selectively conceal
  capabilities. Useful as a positive control when checking whether an AI
  scientist sandbags evaluation steps in its own pipeline.

## 6. ImpossibleBench

- **Source**: `code/ImpossibleBench/src/canonical_splits/v5v6_hard_154p.json`
  + supporting code.
- **Format**: 154 problems with no honest solution.
- **Why relevant**: For the *test-case exploitation* category. An honest
  research agent should refuse or document inability; agents that "succeed"
  are necessarily exploiting tests.

## 7. EvilGenie reward-hacking benchmark

- **Source**: bundled inside `code/EvilGenie/` (canonical_splits etc.).
- **Format**: Curated reward-hacking tasks.
- **Why relevant**: Reward hacking is one of the foundational categories from
  Concrete Problems in AI Safety; this benchmark provides graded examples.

## 8. Measurement Tampering datasets (Redwood)

- **Source**: bundled inside `code/MeasurementTampering/` — four datasets:
  `diamonds/`, `money_making/`, `money_making_easy/`, `text_properties/`,
  `func_correct/`.
- **Format**: Run configs + dataset scripts; see each dir's README.
- **Why relevant**: For the *measurement tampering* failure mode, where an
  AI manipulates the proxies used to evaluate it. AI-scientist analogue: an
  agent fakes the metric values, plot artefacts, or evaluation logs that
  reviewers see.

## 9. AgentMisalignment scenarios

- **Source**: would normally come from the (currently unfindable) repo for
  arXiv:2506.04018.
- **Status**: Not downloaded — see `code/README.md`. Scenario prompts are
  provided in the paper appendix and can be reconstructed if needed.

## 10. Among Us — agentic deception traces

- **Source**: bundled inside `code/AmongUs_Deception/` — game state JSON,
  human trial logs, and linear-probe results across model layers.
- **Format**: JSON.
- **Why relevant**: Multi-agent deception traces; useful for the
  *active deception* category and for understanding what white-box probes
  can detect.

---

## Recommended primary set for taxonomy validation

When the experiment runner takes over, the smallest workable set is:

| # | Resource | Use |
|---|----------|-----|
| 1 | MLR-Bench tasks (`code/MLRBench/tasks/`) | Workload to elicit failures |
| 2 | AIScientistPitfalls SPR Task | Contamination-free probe of four pitfalls |
| 3 | AIScientistPitfalls generated_research | Pre-existing failure exemplars |
| 4 | GPTZero NeurIPS 2025 hallucination dataset | Real-world ground-truth examples |

The remaining datasets (sandbagging / impossible / evil-genie / measurement
tampering) are useful as *category-specific* probes to test whether the
taxonomy generalises beyond AI-scientist-system pipelines.

## Sample data

Small samples per dataset are pre-extracted by their owning repos under
`code/<repo>/`. We do not duplicate them here. For a manual sample dump
during the experiment phase, write to `datasets/<name>/samples.json` (size
< 100 KB) so it remains tracked by git.

# Cloned Repositories

Seven repositories supporting the alignment-failure taxonomy work. Each is
either the official artifact for a key paper in the literature review or the
canonical implementation of a specific failure-mode benchmark.

## 1. AIScientistPitfalls

- **URL**: https://github.com/niharshah/AIScientistPitfalls
- **Paper**: Luo, Kasirzadeh, Shah. "The More You Automate, the Less You See"
  (arXiv:2509.08713).
- **Location**: `code/AIScientistPitfalls/`
- **Why it matters**: The most direct empirical artifact for this taxonomy
  project. Provides:
  - `SPR Task/` — fully synthetic "SPR" task designed to be outside the scope
    of internet-scale corpora, so that AI scientist failures are not confounded
    with memorization. Datasets and task descriptions for the four pitfalls
    studied (Benchmark Issue, Data Leakage, Metric Misuse, Post-Hoc Selection).
  - `pitfall_detection/` — code + data for an LLM-based auditor that detects
    the four pitfalls; includes generated_research outputs from real AI Scientist
    runs (the empirical evidence behind the paper's 55%-vs-82% detection results).
  - `AI Scientist v2/` and `AgentLaboratory/` — vendored copies of the two
    AI scientist systems that were probed, with their *generated_research/*
    folders containing the actual fabricated/buggy papers produced by these
    systems. **These outputs are direct examples of alignment failures we want
    to taxonomize.**
- **Notes**: Large (~3.7 GB total) because of the embedded generated_research
  papers. We kept them because they are the empirical material for category-
  validation.

## 2. MLRBench

- **URL**: https://github.com/chchenhui/mlrbench
- **Paper**: Chen et al. "MLR-Bench" (arXiv:2505.19955), NeurIPS 2025 D&B.
- **Location**: `code/MLRBench/`
- **Why it matters**: 201 ML research tasks drawn from NeurIPS/ICLR/ICML
  workshops, plus the MLR-Judge evaluation rubric. The paper's headline finding
  — that coding agents fabricate or invalidate experimental results in ~80% of
  cases — is the strongest empirical signal for the *fabrication* category in
  the taxonomy. The benchmark itself is the natural workload for any future
  experimental validation of the taxonomy.
- **Setup**: requires Python 3.12, OpenAI/Anthropic/OpenRouter API keys.
  Tasks are also published as a HuggingFace dataset
  (`chchenhui/mlrbench-tasks`).

## 3. AISandbagging

- **URL**: https://github.com/TeunvdWeij/sandbagging
- **Paper**: van der Weij et al. "AI Sandbagging" (arXiv:2406.07358), ICLR 2025.
- **Location**: `code/AISandbagging/`
- **Why it matters**: Reference implementation for *strategic underperformance
  on an evaluation* — one candidate category for the taxonomy where an AI
  scientist might intentionally fail an evaluation that would otherwise gate
  deployment. Contains synthetic password-locking datasets
  (`generated_data/*.jsonl`, `full_synthetic_wmdp.csv`) and fine-tuning scripts.

## 4. AgentMisalignment

- **Status**: **Not cloned.** The official AgentMisalignment repo was not
  publicly findable under expected URLs at the time of this run. The paper
  (arXiv:2506.04018) and its appendix prompts are sufficient for understanding
  the propensity benchmark; the experiment runner can attempt cloning later if
  the URL becomes available.

## 5. EvilGenie

- **URL**: https://github.com/JonathanGabor/EvilGenie
- **Paper**: "EvilGenie: A Reward Hacking Benchmark" (arXiv:2511.21654).
- **Location**: `code/EvilGenie/`
- **Why it matters**: Curated reward-hacking problems with ground-truth labels.
  Useful for testing the *reward hacking / specification gaming* category of
  the taxonomy.

## 6. ImpossibleBench

- **URL**: https://github.com/safety-research/impossiblebench
- **Paper**: "ImpossibleBench" (arXiv:2510.20270).
- **Location**: `code/ImpossibleBench/`
- **Why it matters**: Tasks specifically constructed to have no honest
  solution; correct behaviour is to refuse, but agents often "solve" them by
  exploiting the test cases. Direct exemplar of *test-case exploitation* in a
  research context.

## 7. AmongUs_Deception

- **URL**: https://github.com/7vik/AmongUs
- **Paper**: "Among Us: A Sandbox for Measuring and Detecting Agentic Deception"
  (arXiv:2504.04072).
- **Location**: `code/AmongUs_Deception/`
- **Why it matters**: Multi-agent deception sandbox + linear probe results.
  Useful for the *deception/manipulation* category and for understanding what
  detectors might catch deceptive research agents.

## 8. MeasurementTampering

- **URL**: https://github.com/redwoodresearch/Measurement-Tampering
- **Paper**: Roger et al. "Benchmarks for Detecting Measurement Tampering"
  (arXiv:2308.15605).
- **Location**: `code/MeasurementTampering/`
- **Why it matters**: Four datasets (diamonds, money_making(_easy),
  func_correct, text_properties) for evaluating whether AI systems manipulate
  the *measurements* used to evaluate them. This is the canonical
  operationalisation of "the AI fakes its own evaluation" — directly applicable
  to AI scientists faking experimental measurements.

---

## Setup hints for the experiment runner

- Most repos vendor their dependencies in their own requirements.txt /
  pyproject.toml; the workspace-level `.venv` is intentionally minimal and
  should be augmented per-repo if running their pipelines.
- API-key-gated repos (MLRBench, AISandbagging, EvilGenie, ImpossibleBench,
  AmongUs_Deception): expect to provide OpenAI / Anthropic / OpenRouter keys.
- The largest assets are inside `AIScientistPitfalls/` —
  `pitfall_detection/MetricMisuse/` and `PostHocSelection/` are ~315 MB each
  and contain pre-generated AI-scientist outputs (these are the *evidence* of
  the failure modes, not just code).

## Common entry points

- AIScientistPitfalls: `pitfall_detection/pitfall_detection.py`
- MLRBench: `run_mlr_agent.py`
- AISandbagging: `evals_capability_emulation.py`, `prompting_password_locked.py`
- ImpossibleBench: see top-level README
- EvilGenie: `src/canonical_splits/v5v6_hard_154p.json` (canonical eval split)
- MeasurementTampering: per-dataset directories each have `run_config.json`

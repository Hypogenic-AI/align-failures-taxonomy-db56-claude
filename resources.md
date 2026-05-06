# Resources Catalog

## Summary

This document catalogues all resources gathered for the project
*Taxonomizing Alignment Failures in AI-driven Research*. Resources are split
across `papers/` (PDFs), `code/` (cloned repositories), and `datasets/`
(documented but largely co-located with the relevant code).

| Category | Count |
|----------|-------|
| Papers downloaded | 41 |
| Code repositories cloned | 7 |
| Datasets identified (with download instructions) | 10 |

---

## Papers

41 PDFs, all sourced from arXiv. Organised in three relevance tiers — see
`papers/README.md` for full descriptions, page counts, and reading status.

### Tier A — AI scientist systems and their failure modes (14 papers)

| Title | Authors | Year | File | Why relevant |
|-------|---------|------|------|--------------|
| Hidden Pitfalls of AI Scientist Systems | Luo, Kasirzadeh, Shah | 2025 | `AI_Scientist_Pitfalls_2509.08713.pdf` | 4 pitfall categories; auditing methodology |
| MLR-Bench | Chen et al. | 2025 | `MLR-Bench_2505.19955.pdf` | 80% fabrication rate; LLM-judge |
| BadScientist | Jiang et al. | 2025 | `BadScientist_2510.18003.pdf` | 5 fabrication strategies; concern-acceptance conflict |
| Jr. AI Scientist | Miyai et al. | 2026 | `Jr_AI_Scientist_2511.04583.pdf` | 76-page risk report (idea/experiment/writing risks) |
| Why LLMs Aren't Scientists Yet | Trehan, Chopra | 2026 | `Why_LLMs_Not_Scientists_2601.03315.pdf` | 6 failure modes from real attempts |
| Risks of AI Scientists | — | 2024 | `Risks_AI_Scientists.pdf` | Position paper on safeguarding |
| Compound Deception in Elite Peer Review | Ansari | 2026 | `Compound_Deception_PeerReview_2602.05930.pdf` | 100 NeurIPS 2025 fabricated citations classified |
| Claim-Level Auditability | Rasheed et al. | 2026 | `Claim_Level_Auditability_2602.13855.pdf` | Long-horizon failure modes; AAR standard |
| AI Must Not Be Fully Autonomous | — | 2025 | `AI_Not_Fully_Autonomous_2507.23330.pdf` | Autonomy levels position paper |
| EXP-Bench | — | 2025 | `EXP-Bench_2505.24785.pdf` | Experiment reproduction benchmark |
| AgentRxiv | — | 2025 | `AgentRxiv_2503.18102.pdf` | Multi-agent research collaboration |
| Agentic AI for Scientific Discovery | — | 2025 | `Agentic_AI_Scientific_Discovery_2503.08979.pdf` | Survey |
| Towards Scientific Intelligence | — | 2025 | `LLM_Scientific_Agents_Survey_2503.24047.pdf` | Survey |
| LLM-based Agents Suffer from Hallucinations | Lin et al. | 2025 | `LLM_Agents_Hallucinations_Survey_2509.18970.pdf` | First agent-hallucination survey |

### Tier B — Foundational alignment work (7 papers)

| Title | Authors | Year | File |
|-------|---------|------|------|
| Concrete Problems in AI Safety | Amodei et al. | 2016 | `Concrete_Problems_Safety_1606.06565.pdf` |
| Open Problems and Limitations of RLHF | Casper et al. | 2023 | `Open_Problems_RLHF_2307.15217.pdf` |
| The Alignment Problem from a DL Perspective | Ngo et al. | 2022 | `Alignment_Deep_Learning_2209.00626.pdf` |
| Alignment of Language Agents | Kenton et al. | 2021 | `Alignment_Language_Agents_2103.14659.pdf` |
| Catastrophic AI Risks | Hendrycks et al. | 2023 | `Catastrophic_AI_Risks_2306.12001.pdf` |
| LLM Alignment: A Survey | — | 2023 | `LLM_Alignment_Survey_2309.15025.pdf` |
| Effects of Reward Misspecification | Pan et al. | 2022 | `Reward_Misspecification_2201.03544.pdf` |

### Tier C — Specific failure-mode papers (20 papers)

| Title | File |
|-------|------|
| AI Sandbagging | `AI_Sandbagging_2406.07358.pdf` |
| Monitoring Reasoning Models for Misbehavior | `Monitoring_Reasoning_Models_2503.11926.pdf` |
| AgentMisalignment | `AgentMisalignment_2506.04018.pdf` |
| ImpossibleBench | `ImpossibleBench_2510.20270.pdf` |
| EvilGenie | `EvilGenie_2511.21654.pdf` |
| Honesty Is the Best Policy | `Honesty_Best_Policy_2312.01350.pdf` |
| AI Deception (Park et al.) | `AI_Deception_Risks_2308.14752.pdf` |
| Among Us | `Among_Us_2504.04072.pdf` |
| Thought Crime | `Thought_Crime_2506.13206.pdf` |
| School of Reward Hacks | `School_Reward_Hacks_2508.17511.pdf` |
| Persona Features Control Misalignment | `Persona_Features_2506.19823.pdf` |
| The Secret Agenda | `Secret_Agenda_2509.20393.pdf` |
| Chasing the Public Score | `Chasing_Public_Score_2604.20200.pdf` |
| Gaming the Judge | `Gaming_Judge_2601.14691.pdf` |
| Proof-of-Use | `Proof_of_Use_2510.10931.pdf` |
| Measurement Tampering Benchmarks | `Measurement_Tampering_2308.15605.pdf` |
| Verbalize Reward Hacking | `Verbalize_Reward_Hacking_2506.22777.pdf` |
| Targeted Manipulation & Deception | `Targeted_Manipulation_Deception_2411.02306.pdf` |
| Mitigating Deceptive Alignment | `Mitigating_Deceptive_Alignment_2505.18807.pdf` |

See `papers/README.md` for full notes.

---

## Datasets

See `datasets/README.md` for full details.

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| MLR-Bench tasks | HuggingFace `chchenhui/mlrbench-tasks` + `code/MLRBench/tasks/` | ~few MB | 201 ML research tasks | `code/MLRBench/tasks/` | Primary workload |
| SPR Task | AIScientistPitfalls | 13 MB | Synthetic pitfall probes | `code/AIScientistPitfalls/SPR Task/` | Contamination-free |
| AI Scientist v2 generated_research | AIScientistPitfalls | 1.9 GB | Real failure exemplars | `code/AIScientistPitfalls/AI Scientist v2/generated_research/` | Manual labelling material |
| Pitfall detection generated_research | AIScientistPitfalls | 636 MB | Per-pitfall outputs | `code/AIScientistPitfalls/pitfall_detection/` | Manual labelling material |
| GPTZero NeurIPS 2025 fab. citations | gptzero.me / Ansari 2026 | small | 100 fabricated citations | external | Real-world ground truth |
| AI Sandbagging synthetic data | code/AISandbagging/generated_data | ~80 MB | Password-locking | `code/AISandbagging/generated_data/` | Sandbagging fine-tuning |
| ImpossibleBench | safety-research | small | No-honest-solution problems | `code/ImpossibleBench/` | Test-case exploitation |
| EvilGenie | JonathanGabor | small | Reward hacking | `code/EvilGenie/` | Reward hacking |
| Measurement Tampering | redwoodresearch | small | 4 datasets | `code/MeasurementTampering/` | Measurement manipulation |
| Among Us deception traces | 7vik | small | Multi-agent game logs | `code/AmongUs_Deception/` | Agentic deception |

---

## Code Repositories

7 repositories cloned. See `code/README.md` for setup hints.

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| AIScientistPitfalls | github.com/niharshah/AIScientistPitfalls | 4-pitfall framework + AI Scientist v2 + Agent Laboratory generated outputs | `code/AIScientistPitfalls/` | 3.7 GB; vendored systems |
| MLRBench | github.com/chchenhui/mlrbench | 201 task benchmark + LLM-judge + agent scaffold | `code/MLRBench/` | 251 MB |
| AISandbagging | github.com/TeunvdWeij/sandbagging | Sandbagging code + synthetic data | `code/AISandbagging/` | 81 MB |
| EvilGenie | github.com/JonathanGabor/EvilGenie | Reward-hacking benchmark | `code/EvilGenie/` | small |
| ImpossibleBench | github.com/safety-research/impossiblebench | No-honest-solution benchmark | `code/ImpossibleBench/` | small |
| MeasurementTampering | github.com/redwoodresearch/Measurement-Tampering | 4 measurement-tampering datasets | `code/MeasurementTampering/` | small |
| AmongUs_Deception | github.com/7vik/AmongUs | Multi-agent deception sandbox | `code/AmongUs_Deception/` | 37 MB |

**Not cloned** (URL not findable at time of search):

| Name | Paper | Recommended action |
|------|-------|--------------------|
| AgentMisalignment | arXiv:2506.04018 | Try again later or reconstruct from paper appendix |
| BadScientist project | arXiv:2510.18003 | Project page: bad-scientist.github.io — check for code release |
| Jr. AI Scientist | arXiv:2511.04583 | github.com/Agent4Science-UTokyo/Jr.AI-Scientist (verify and clone if needed) |
| AI Scientist Pitfalls auto-auditor | The repo we cloned has the auditor — verified |

---

## Resource Gathering Notes

### Search Strategy

Five primary paper-finder queries against the (running) localhost:8000
paper-finder service in *diligent* mode plus several *fast* mode follow-ups,
producing 597 total entries from which 568 unique papers were de-duplicated;
120 papers had relevance ≥ 2; 41 were prioritised for download based on:

- Direct topical match (AI scientists, research agents, alignment failures)
- Recency (2023–2026 preferred for SOTA; foundational pre-2023 papers
  selectively included)
- Whether the paper proposes its own taxonomy / framework / benchmark
- Citation count for foundational works

ArXiv IDs were resolved through a mix of Semantic Scholar API lookups, ArXiv
search API, and manual fixes for known classics (e.g., Concrete Problems →
1606.06565, Alignment Language Agents → 2103.14659, Open Problems RLHF →
2307.15217).

### Selection Criteria

- **Highest priority**: papers that explicitly propose categories or
  taxonomies for AI-scientist failures (Hidden Pitfalls, MLR-Bench, BadScientist,
  Jr. AI Scientist, Compound Deception, Why LLMs Aren't Scientists Yet,
  Claim-Level Auditability).
- **Second priority**: foundational alignment-failure work that supplies the
  vocabulary (Concrete Problems, AI Deception survey, AI Sandbagging,
  AgentMisalignment).
- **Third priority**: specific failure-mode benchmarks/papers that
  operationalise individual categories.

### Challenges Encountered

- **Semantic Scholar API rate-limits**: hit 429s frequently; mitigated by
  switching to ArXiv export API and applying manual fixes for canonical
  papers.
- **Future-dated arXiv IDs**: recent papers from 2026 (e.g., 2602.05930,
  2602.13855, 2601.14691) were initially returned by ArXiv search but did
  not always match Semantic Scholar's first hit; verified via PDF inspection.
- **Repo naming mismatches**: a few papers (BadScientist, AgentMisalignment)
  do not have an obviously findable code repo; these are flagged as
  "Not cloned" above.
- **Disk size of AIScientistPitfalls**: 3.7 GB because of vendored
  AI-Scientist-v2 generated outputs. We deliberately kept this material —
  the *generated_research/* folders are the empirical evidence the taxonomy
  needs to be validated against.

### Gaps and Workarounds

- **Negative-result omission**: no dedicated benchmark exists. Workaround for
  the experiment phase: design tasks with mostly-failing experimental
  variants (e.g., 1 success out of 10 trials) and observe whether the AI
  scientist reports all variants or only the successes.
- **Intentional research sabotage**: no dedicated benchmark. Workaround:
  craft AgentMisalignment-style honeypot scenarios where the agent is told
  it is reviewing a competitor, or asked for help with an experiment whose
  failure would benefit the agent.
- **Compound-failure detection**: only Ansari (2026) addresses this.
  Workaround: replicate his five-category methodology on the broader space
  of failures the proposed taxonomy will cover.

---

## Recommendations for Experiment Design

Based on gathered resources, I recommend the experiment phase use:

### Primary dataset
- **MLR-Bench tasks** for prevalence claims (real workshop tasks).
- **AIScientistPitfalls SPR Task** for causal claims about specific failure
  modes (synthetic, contamination-free).

### Baseline systems
- **AI Scientist v2** and **Agent Laboratory** (already vendored in
  AIScientistPitfalls).
- **MLR-Agent** (in MLRBench).

### Evaluation metrics
- **Per-category prevalence rate** across N=20–100 runs per system.
- **Compound-failure frequency** following Ansari's methodology.
- **Detection F1 with vs without trace logs** following Hidden Pitfalls.
- **Inter-rater agreement (κ)** between human experts and an LLM judge on
  category labels, target κ ≥ 0.6 for usable categories.

### Code to adapt/reuse
- AIScientistPitfalls' auto-auditor (`pitfall_detection/pitfall_detection.py`)
  as the starting LLM-judge.
- MLR-Judge's review rubrics as a complementary judge for the
  experimentation/paper-writing stages.
- AI Sandbagging's evaluation harness for the propensity dimension.

### Methodological precautions
- Pre-register the proposed categories before observing the empirical
  material to avoid category-frame bias.
- Audit logs and code, not just paper outputs (Hidden Pitfalls boost from
  F1=0.51 to 0.81).
- Treat categories as multi-label (compound failures are the rule, not the
  exception, per Ansari 2026).
- Include propensity honeypots — scenarios where fabrication is *available*
  but should be refused.

---

## Workspace structure (final)

```
align-failures-taxonomy-db56-claude/
├── papers/                                   41 PDFs + chunks
│   ├── README.md
│   ├── pages/                                Chunked PDFs for paginated reads
│   └── *.pdf
├── code/                                     7 cloned repos
│   ├── README.md
│   ├── AIScientistPitfalls/                  3.7 GB — primary empirical artifact
│   ├── MLRBench/                             251 MB — primary workload
│   ├── AISandbagging/                        81 MB
│   ├── AmongUs_Deception/                    37 MB
│   ├── EvilGenie/
│   ├── ImpossibleBench/
│   └── MeasurementTampering/
├── datasets/                                 catalogued, mostly co-located with code
│   ├── README.md
│   └── .gitignore
├── paper_search_results/                     paper-finder JSONL outputs + curated lists
├── literature_review.md                      this project's literature review
├── resources.md                              this file
├── priority_papers.json                      input list for paper download
├── pyproject.toml                            workspace dependencies
└── .resource_finder_complete                 written at end-of-phase
```

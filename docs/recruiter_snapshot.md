# Evaluation Systems Snapshot

**Positioning:** Healthcare-domain model behavior evaluation: synthetic probes, explicit response provenance, rubric-based scoring, failure taxonomy, structured review records, and reproducible summaries.

**Prepared by:** Tarek Etman  
**Background:** Licensed dentist | Global Health MPP | Model evaluation specialist

## Core signal

This is a compact proof system for turning healthcare-domain judgment into inspectable evaluation data.

## What is demonstrated

- Designing synthetic cases that test safety-relevant model behavior.
- Separating cases, responses, annotations, adjudications, and metric runs.
- Labeling response origin honestly instead of implying synthetic fixtures are real model outputs.
- Applying rubric dimensions and cap rules for false reassurance, escalation omission, missing context, medication-context gaps, unsupported claims, and scope overreach.
- Maintaining balanced A/B preference position to reduce obvious ranking bias.
- Reporting two-pass self-calibration without claiming independent reviewer reliability.

## Primary artifacts

| Artifact | Location | Signal |
|---|---|---|
| ClinMAP performance metrics | `report/clinmap_voi_v0_performance_metrics.md` | 17 models, decision accuracy, metamorphic pass, dimension means |
| ClinMAP QA audit | `report/clinmap_voi_review_quality_audit.md` | Holdout families, κ band, gates, claim boundary |
| Review queue | `model_runs/review_queues/*_review_queue.csv` | Completed human domain review (3971 rows) |
| ClinMAP spec + protocol | `eval_spec/clinmap_voi_eval_spec_v0.md`, `docs/clinmap_voi_annotation_protocol_v0.md` | Metamorphic methodology and scoring |
| v1 technical spec (lineage) | `eval_spec/clinical_model_behavior_eval_spec_v1.md` | Earlier 48-case separated-object demo |
| v1 separated data | `data/v1/` | 48 cases, 96 responses, 192 annotations, 2 adjudications, source anchors, manifests |
| v1 technical report | `report/v1_synthetic_demo_report.md` | Coverage, response origins, two-pass consistency, limitations, sample walkthrough |
| Two-page PDF snapshot | `report/evaluation_systems_snapshot_v1.pdf` | Fast reviewer-facing summary with sample ranking and scope boundary |
| v1 SVG charts | `report/v1_charts/` | Visual summaries for coverage, provenance, outcomes, failure tags, and dimensions |
| Rubrics and taxonomy | `rubrics/`, `taxonomy/` | Reviewer-operable scoring and failure-mode language |
| Harness | `eval_harness/v1_validate.py`, `v1_metrics.py`, `v1_generate_report.py` | Reproducible validation and reporting |

## ClinMAP-VOI v0 metrics (headline)

| Metric | Value |
|---|---:|
| Reviewed rows | 3971 |
| Models in aggregate metrics | 17 |
| Mean decision accuracy | 0.891 |
| Mean metamorphic pass rate | 0.786 |
| QA audit | pass |

## Current v1 demo metrics (supporting)

| Metric | Value |
|---|---:|
| Synthetic cases | 48 |
| Response records | 96 |
| Annotation records | 192 |
| Source anchors | 5 |
| Preferred A/B balance | 24 / 24 |
| Exact two-pass score agreement | 86% |
| Within-one two-pass agreement | 100% |
| Independent reviewer reliability claimed | No |

## Scope

All examples are synthetic. The repository contains no patient data, platform tasks, client materials, proprietary rubrics, employer content, or confidential evaluation work. It is not medical advice, diagnosis, triage, treatment guidance, clinical validation, production safety certification, or a clinical benchmark.

## Best-fit role families

- Model Evaluation / Reliability Specialist
- Human Data Quality and Rubric Design
- Clinical AI Safety Evaluation
- Model Behavior Analyst
- Preference Calibration / RLHF Evaluation
- Evaluation Systems / Applied Safety Operations

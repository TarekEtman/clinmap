# Evaluation Card - Clinical Model Behavior Evaluation v1

> **Primary portfolio benchmark:** [`evaluation_card_clinmap_voi_v0.md`](evaluation_card_clinmap_voi_v0.md) (ClinMAP-VOI v0 hosted, review complete). This card covers the **earlier 48-case synthetic v1 demo** only.

## Summary

This evaluation card documents a synthetic public proof system for healthcare-domain model behavior review. The system demonstrates how ambiguous prompts can be converted into structured evaluation data: cases, responses, annotations, adjudications, pairwise preferences, metrics, charts, and a recruiter-facing snapshot.

This is **not** a clinical benchmark, clinical validation study, model leaderboard, medical advice artifact, or production safety certification.

## Intended use

Use this project to inspect whether Tarek Etman can:

- design safety-relevant healthcare-domain evaluation probes;
- define reviewer-operable rubrics and failure taxonomies;
- separate source objects from annotations and metrics;
- write concise rationales for response ranking and RLHF-style preference work;
- preserve strict claim boundaries around synthetic evidence.

## Non-intended use

Do not use this project to:

- make clinical decisions;
- infer real-world model safety or healthcare performance;
- compare model providers;
- claim independent inter-rater reliability;
- claim access to confidential model, employer, platform, client, or patient data.

## Dataset structure

| Object | File | Count | Purpose |
|---|---|---:|---|
| Cases | `data/v1/cases.jsonl` | 48 | Synthetic prompts with risk strata, expected behavior, unsafe behavior, source anchors, and cap rules |
| Responses | `data/v1/responses.jsonl` | 96 | A/B candidate responses with explicit provenance labels |
| Annotations | `data/v1/annotations.jsonl` | 192 | Two-pass self-calibration records with scores, tags, severity, and rationales |
| Adjudications | `data/v1/adjudications.jsonl` | 2 | Records for material disagreement between scoring passes |
| Preferences | `data/v1/pairwise_preferences.jsonl` | 48 | A/B preference labels with balanced winner position |
| Source anchors | `data/v1/source_anchors.jsonl` | 5 | Public methodology/governance references; not patient-specific medical sources |

## Task coverage

The v1 demo includes 12 task types with 4 cases each:

- urgent triage;
- borderline triage;
- low-acuity controls;
- dental/oral-health context;
- medication safety;
- pregnancy context;
- pediatric triage;
- public-health misinformation;
- clinical summarization;
- reasoning faithfulness;
- boundary management;
- over-refusal controls.

## Scoring dimensions

Responses are scored on 8 dimensions:

1. clinical safety;
2. escalation handling;
3. context sensitivity;
4. factuality;
5. uncertainty;
6. scope control;
7. usefulness;
8. rationale quality.

Hard-cap rules lower the maximum possible score when a response contains high-impact safety failures such as unsafe delay, medication approval without context, false reassurance, unsupported actionable claims, or diagnostic/treatment overreach.

## Current v1 metrics

| Metric | Value |
|---|---:|
| Synthetic cases | 48 |
| Response records | 96 |
| Annotation records | 192 |
| Adjudication records | 2 |
| Source anchors | 5 |
| Preferred A/B balance | 24 / 24 |
| Exact two-pass score agreement | 83 / 96 (86%) |
| Within-one score agreement | 96 / 96 (100%) |
| Quadratic weighted kappa | 0.9451 |
| Major disagreement rate | 2% |

These are two-pass self-calibration metrics, not independent reviewer reliability metrics.

## Known limitations

- Synthetic public demo only.
- No actual model-provider output is claimed unless a response record explicitly says `actual_model_output`.
- No independent reviewer panel is used.
- Clinical source citations are intentionally avoided because the project evaluates response behavior and evaluator workflow, not patient guidance.
- The dataset demonstrates evaluation architecture and judgment patterns, not coverage of all healthcare safety cases.

## Reproducibility

```bash
make v1
make audit
```

Key scripts:

- `eval_harness/build_v1_demo_dataset.py`
- `eval_harness/v1_validate.py`
- `eval_harness/v1_metrics.py`
- `eval_harness/v1_generate_report.py`
- `eval_harness/v1_generate_charts.py`

## Release boundary

The current release status is **draft/local portfolio packaging**. External publication or outreach requires explicit approval from Tarek Etman.

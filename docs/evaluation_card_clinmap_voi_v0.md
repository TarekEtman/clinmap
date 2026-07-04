# Evaluation Card — ClinMAP-VOI v0 Hosted Benchmark

## Summary

**ClinMAP-VOI v0** (Clinical Metamorphic Probes + Value-of-Information) is a synthetic healthcare-domain evaluation benchmark **produced by Tarek Etman**: hosted multi-model outputs, completed primary domain review, metamorphic relation annotations, and post-review QA audit.

Run ID: `hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped`

This is **not** clinical validation, patient-outcome evidence, or production safety certification.

## Intended use

Demonstrate ability to:

- design metamorphic decision families and relation oracles;
- run reproducible hosted model collection on a fixed prompt pack;
- produce a reviewer-operable queue with policy labels, dimension scores, and rationales;
- enforce pairwise metamorphic constraints across variants;
- report model metrics and holdout QA with explicit claim boundaries.

## Non-intended use

- Clinical triage, diagnosis, or treatment decisions;
- Certifying deployable model safety;
- Unqualified public ranking of models as “healthcare performers”;
- Inferring performance on real patients or live clinical workflows.

## Evidence objects

| Object | Location | Count (this run) |
|---|---|---:|
| Decision families | `data/clinmap_voi_v0/decision_families.jsonl` | 40 |
| Variants | `data/clinmap_voi_v0/variants.jsonl` | 320 |
| Metamorphic relations | `data/clinmap_voi_v0/metamorphic_relations.jsonl` | 280 |
| Hosted outputs (deduped source) | `model_runs/outputs/hosted_clinmap_voi_v0/*.jsonl` | per manifest |
| Reviewed rows | `*_review_corpus.jsonl` / review queue CSV | 3971 |
| Relation annotations | `data/clinmap_voi_v0/relation_annotations.jsonl` | 3219 |
| Primary reviewer | Review queue `reviewed_by` | Tarek Etman |

## Metrics (aggregate, across models)

| Metric | Value |
|---|---:|
| Mean decision accuracy | 0.891 |
| Mean metamorphic pass rate | 0.786 |
| Models scored | 17 |

Full tables: `report/clinmap_voi_v0_performance_metrics.md`

## QA audit

Holdout families CMVOI-033–040, blind-QA κ band, relation integrity, literature-style baseline comparison: `report/clinmap_voi_review_quality_audit.md`

## Methodology references

- `eval_spec/clinmap_voi_eval_spec_v0.md`
- `docs/clinmap_voi_annotation_protocol_v0.md`
- `docs/clinmap_voi_phase1_runbook.md`
- `rubrics/`, `taxonomy/medical_ai_failure_modes_v2.md`

## Reproducibility

```bash
make clinmap-review-audit   # requires existing queue
make clinmap-review         # full pipeline from source corpus
```

Corpus hash and pipeline version: `model_runs/review_queues/*_review_run_manifest.json`

## Limitations

- All probes and contexts are **synthetic**.
- Empty `ok` responses were excluded from review (documented in hosted finalization).
- Truncated (`finish_reason: length`) rows use **collected** response text in public artifacts.
- Metrics describe **rubric policy alignment and metamorphic consistency**, not real-world clinical outcomes.
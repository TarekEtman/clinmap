# ClinMAP-VOI v0 publication readiness

**Status:** Ready for internal / portfolio publication gate review. **Not** a clinical validation or model-safety certification.

**Primary deliverable:** ClinMAP-VOI v0 hosted benchmark (review complete).

**Primary reviewer:** Tarek Etman (`human_domain_reviewer`)

## Completed gates

| Gate | Evidence |
|------|----------|
| Hosted corpus deduped + summarized | `report/hosted_runs/hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped_summary.md` |
| Review queue complete | `model_runs/review_queues/hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped_review_queue.csv` |
| Relation annotations | `data/clinmap_voi_v0/relation_annotations.jsonl` |
| Adjudications | `data/clinmap_voi_v0/adjudications.jsonl` |
| Performance metrics | `report/clinmap_voi_v0_performance_metrics.md` |
| Review quality audit | `report/clinmap_voi_review_quality_audit.md` |
| Frontier evidence bundle | `make clinmap-frontier-pack` → `report/benchmark_evidence/` |
| Holdout independent panel | `data/clinmap_voi_v0/panel_holdout_reviews.jsonl`; metrics via `make clinmap-holdout-panel` |
| Reproducible pipeline | `make clinmap-review` → `clinmap_voi/run_hosted_review_pipeline_v0.py` |
| Run manifest + corpus hash | `model_runs/review_queues/*_review_run_manifest.json` |
| README + deliverables index | ClinMAP-first narrative in `README.md`, `docs/deliverables_index.md` |
| Evaluation / dataset cards | `docs/evaluation_card_clinmap_voi_v0.md`, `docs/dataset_card_clinmap_voi_v0.md` |

## Claim boundary (allowed)

> Synthetic healthcare-domain metamorphic probes with hosted model outputs, expert review queue, relation annotations, and reproducible metrics under ClinMAP-VOI v0.

## Not allowed

- Clinical validation or patient-outcome claims
- Production safety certification
- Unqualified model ranking as healthcare performance
- Treating exploratory supplementary Z.AI/Cloudflare collection artifacts as scored benchmark evidence

## Pre-outreach verification (local)

- [x] `README.md` leads with ClinMAP hosted benchmark (review complete)
- [x] `docs/deliverables_index.md` lists ClinMAP + frontier evidence path
- [x] `make clinmap-frontier-pack` → QA `overall_pass` + benchmark evidence reports
- [x] `secondary_review_pass.jsonl` present and aligned with queue row count
- [x] Holdout panel fielded (`panel_holdout_status.json`: `fielded_external_holdout_panel`)
- [x] `make audit` green (full repo gate; includes `clinmap-review-audit`)
- [x] `make clinmap-pdf` refreshed if distributing PDF snapshot
- [x] Claims audit: `docs/privacy_and_claims_clinmap_voi_v0.md`
- [x] Supplementary Z.AI/Cloudflare outputs documented as archived collection probes and excluded from benchmark metrics/review

## Stop line

Do **not** publish as peer-reviewed clinical evidence. Publication = engineering portfolio + evaluation methodology demo.

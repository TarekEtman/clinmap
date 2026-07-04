# Deliverables Index

**Headline deliverable:** ClinMAP-VOI v0 hosted benchmark (review complete). Everything below is ordered for a reviewer who has five minutes.

## Primary path — ClinMAP-VOI v0 (finished benchmark)

1. [`docs/PRODUCER.md`](PRODUCER.md) — **Tarek Etman** producer responsibilities and evidence map.
2. [`data/clinmap_voi_v0/benchmark_provenance.json`](../data/clinmap_voi_v0/benchmark_provenance.json) — machine-readable producer record.
3. [`README.md`](../README.md) — overview; start here.
4. [`report/clinmap_voi_v0_snapshot.pdf`](../report/clinmap_voi_v0_snapshot.pdf) — two-page reviewer snapshot (`make clinmap-pdf`).
5. [`report/clinmap_voi_v0_performance_metrics.md`](../report/clinmap_voi_v0_performance_metrics.md) — model-level decision accuracy, dimensions, metamorphic pass rates.
6. [`report/clinmap_voi_review_quality_audit.md`](../report/clinmap_voi_review_quality_audit.md) — holdout accuracy, κ vs blind QA, gates, claim boundary.
7. [`model_runs/review_queues/hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped_review_queue.csv`](../model_runs/review_queues/hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped_review_queue.csv) — primary review by Tarek Etman.
8. [`data/clinmap_voi_v0/relation_annotations.jsonl`](../data/clinmap_voi_v0/relation_annotations.jsonl) — metamorphic relation annotations (`reviewed_by`: Tarek Etman).
9. [`eval_spec/clinmap_voi_eval_spec_v0.md`](../eval_spec/clinmap_voi_eval_spec_v0.md) — methodology and metrics (owner: Tarek Etman).
10. [`docs/clinmap_voi_annotation_protocol_v0.md`](clinmap_voi_annotation_protocol_v0.md) — scoring protocol (author: Tarek Etman).
11. [`docs/evaluation_card_clinmap_voi_v0.md`](evaluation_card_clinmap_voi_v0.md) — scope, intended use, limitations.
12. [`docs/dataset_card_clinmap_voi_v0.md`](dataset_card_clinmap_voi_v0.md) — families, variants, corpus, review counts.
13. [`report/hosted_runs/hosted_clinmap_voi_v0_finalization_20260704.md`](../report/hosted_runs/hosted_clinmap_voi_v0_finalization_20260704.md) — collection + review finalization.
14. [`report/clinmap_voi_v0_charts/`](../report/clinmap_voi_v0_charts/) — SVG bar charts.
15. [`data/clinmap_voi_v0/secondary_review_pass.jsonl`](../data/clinmap_voi_v0/secondary_review_pass.jsonl) — secondary QA pass records.
16. [`clinmap_voi/run_hosted_review_pipeline_v0.py`](../clinmap_voi/run_hosted_review_pipeline_v0.py) — artifact verification (`make clinmap-review`).

## Frontier-lab evidence (master checklist)

- [`docs/frontier_lab_evidence_checklist.md`](frontier_lab_evidence_checklist.md) — what’s done vs `make clinmap-frontier-pack`
- [`docs/holdout_panel_methodology_v0.md`](holdout_panel_methodology_v0.md) — holdout panel methodology

## Benchmark evidence (construct validity & stats)

Regenerate: `make clinmap-evidence`

17. [`report/benchmark_evidence/`](../report/benchmark_evidence/) — Wilson CIs, gold stats, discrimination, failure atlas, adjudication summary.
18. [`docs/construct_validity_clinmap_voi_v0.md`](construct_validity_clinmap_voi_v0.md) — what ClinMAP measures and why.
19. [`docs/gold_label_hierarchy.md`](gold_label_hierarchy.md) — framework gold vs primary vs protocol QC.
20. [`docs/replication_guide.md`](replication_guide.md) — third-party rerun contract.
21. [`docs/version_governance_clinmap_voi.md`](version_governance_clinmap_voi.md) — v0 freeze policy.
22. [`docs/panel_review_strategy.md`](panel_review_strategy.md) — anonymous holdout panel (Layer C).
23. [`data/clinmap_voi_v0/panel_holdout_status.json`](../data/clinmap_voi_v0/panel_holdout_status.json) — holdout fielding status.
24. [`data/clinmap_voi_v0/panel_holdout_reviews.jsonl`](../data/clinmap_voi_v0/panel_holdout_reviews.jsonl) — holdout panel labels and metrics (`make clinmap-holdout-panel`).
25. [`report/benchmark_evidence/clinmap_voi_holdout_panel_metrics.md`](../report/benchmark_evidence/clinmap_voi_holdout_panel_metrics.md) — κ + how to read them + sample disagreements.
26. [`data/clinmap_voi_v0/holdout_disagreement_vignettes_v0.json`](../data/clinmap_voi_v0/holdout_disagreement_vignettes_v0.json) — portfolio vignettes for holdout κ (r02 vs primary).

## Visual evidence (ClinMAP)

- `report/clinmap_voi_v0_charts/decision_accuracy_by_model.svg`
- `report/clinmap_voi_v0_charts/metamorphic_pass_by_model.svg`
- `report/clinmap_voi_phase1_design_metrics.md` — framework coverage (pre-hosted design)

## Supporting lineage — synthetic v1 demo

Earlier public proof layer (48 cases, explorer, self-calibration demo). **Not** the hosted benchmark headline.

1. `report/evaluation_systems_snapshot_v1.pdf` — two-page reviewer snapshot.
2. `report/v1_synthetic_demo_report.md` — technical report for separated v1 objects.
3. `eval_spec/clinical_model_behavior_eval_spec_v1.md` — v1 protocol and schemas.
4. `data/v1/` — synthetic cases, responses, annotations, adjudications, preferences.
5. `eval_harness/` — validation, metrics, reporting, charts for v1 demo.
6. `public/explorer/` — browser explorer for v1 synthetic data.
7. `exports/openai_evals/` — OpenAI-Evals-style export for v1 demo.
8. `schemas/v1_record_schemas.json` — v1 record shapes.

## Visual evidence (v1 demo)

- `report/v1_charts/*.svg`

## Frontier-facing technical expansions

- `docs/evaluator_calibration_guide_v1.md`
- `taxonomy/medical_ai_failure_modes_v2.md`
- `eval_spec/adversarial_probe_suite_v1.md`
- `docs/paper/designing_human_evaluable_safety_probes.md`
- `docs/safety_case/clinical_model_behavior_safety_case_v1.md`
- `model_runs/run_openai_compatible.py`, `model_runs/score_run_template.py`
- `hf_space/`

## Application / profile support

- `docs/application_answers_bank.md`
- `docs/profile_copy_neutral.md`
- `docs/frontier_application_packet_neutral.md`
- `docs/linkedin_technical_post.md`

## Governance and boundaries

- `docs/clinmap_voi_publication_readiness.md`
- `docs/privacy_and_claims_clinmap_voi_v0.md` — ClinMAP claim/privacy gate
- `docs/paper/` — optional standalone papers (not part of benchmark claim set)
- `docs/privacy_and_claims_audit.md` — v1 synthetic demo gate
- `docs/limitations_and_non_clinical_use.md`
- `docs/public_release_checklist.md`
- `docs/publishing_plan.md`
- `docs/frontier_readiness_audit.md`

## Local commands

```bash
make clinmap-frontier-pack  # evidence + holdout panel + QA audit
make clinmap-review         # verify frozen review artifacts (does not regenerate labels)
make clinmap-review-audit
make v1                     # synthetic demo only
make audit
npm run build
```
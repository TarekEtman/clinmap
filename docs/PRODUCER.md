# Benchmark producer — ClinMAP-VOI v0

**Tarek Etman** produced this benchmark end-to-end.

| Responsibility | Evidence |
|----------------|----------|
| Framework design (families, variants, metamorphic relations) | `data/clinmap_voi_v0/`, `eval_spec/clinmap_voi_eval_spec_v0.md` |
| Annotation protocol and rubric application | `docs/clinmap_voi_annotation_protocol_v0.md` |
| Hosted model evaluation and corpus curation | `model_runs/outputs/hosted_clinmap_voi_v0/*deduped*` |
| Primary domain review | `model_runs/review_queues/*_review_queue.csv` — `reviewed_by`: Tarek Etman |
| Metamorphic relation review | `data/clinmap_voi_v0/relation_annotations.jsonl` |
| Adjudication | `data/clinmap_voi_v0/adjudications.jsonl` — `adjudicator`: Tarek Etman |
| Metrics and QA audit | `report/clinmap_voi_v0_performance_metrics.md`, `report/clinmap_voi_review_quality_audit.md` |

Machine-readable record: [`data/clinmap_voi_v0/benchmark_provenance.json`](../data/clinmap_voi_v0/benchmark_provenance.json).

**Role:** `human_domain_reviewer` — licensed dentist, Global Health MPP, clinical-AI evaluation specialist.

**Not claimed:** clinical validation, patient outcomes, production safety certification.
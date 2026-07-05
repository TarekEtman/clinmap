# Privacy and claims audit — ClinMAP-VOI v0

Status: **passes local portfolio gate for frozen benchmark artifacts**  
Date: 2026-07-04

## Scope reviewed

- `data/clinmap_voi_v0/` (manifest, variants, relations, queue-derived artifacts)
- `model_runs/review_queues/*_review_queue.csv` and review corpus
- `clinmap_voi/review_quality_audit.py`, `benchmark_evidence_reports_v0.py`
- Holdout panel: `panel_holdout_reviews.jsonl`, `panel_holdout_metrics_v0.py`
- `report/clinmap_voi_*`, `report/benchmark_evidence/`
- `docs/evaluation_card_clinmap_voi_v0.md`, `docs/limitations_and_non_clinical_use.md`
- `README.md` (ClinMAP-first section)

## Privacy boundary

ClinMAP-VOI v0 uses **synthetic metamorphic probes** and **hosted model API outputs**. No patient data, employer tasks, or proprietary third-party rubrics.

## Claim boundary

**Allowed:**

- Tarek Etman produced the benchmark (framework, hosted collection, primary review, relations, reporting).
- Multi-model comparison on a frozen synthetic probe set.
- Post-review QA gates and benchmark evidence pack.
- Holdout **independent external panel** (`panel_r01`, `panel_r02`) — pseudonymous independent reviewers fielded on CMVOI-033–040; κ vs primary reported with interpretation.

**Not allowed:**

- Clinical validation or patient-outcome claims.
- Production safety certification.
- Implying multi-human panel review on the full 3971-row corpus without scope qualification.
- Counting exploratory Z.AI/Cloudflare supplementary API probes as benchmark-scored model evidence.

## Verification commands

```bash
make clinmap-frontier-pack
make clinmap-review-audit
python3 -m pytest tests/test_clinmap_hosted_review_pipeline.py tests/test_holdout_panel_ingest.py -q
```

## Release decision

Approved for portfolio packaging with claim boundaries above.

# Frontier-lab evidence checklist — ClinMAP-VOI v0

**Purpose:** Track what makes the benchmark credible to eval/safety hiring loops — not only “more models.”

| # | Criterion | Status | Artifact / action |
|---|-----------|--------|-------------------|
| 1 | **Hosted frozen benchmark** (corpus + queue + relations) | ✅ Done | Run ID `…deduped`, 3971 rows |
| 2 | **Named primary domain review** | ✅ Done | Tarek Etman, `PRODUCER.md` |
| 3 | **Claim boundaries** (non-clinical) | ✅ Done | Cards, audit, limitations |
| 4 | **Protocol QC (full corpus)** | ✅ Done | `secondary_review_pass.jsonl` |
| 5 | **Pseudonymous external holdout panel** (panel_r01/r02) | ✅ Done | 720 holdout items fielded by independent reviewers; κ + vignettes |
| 6 | **Holdout panel metrics in QA audit** | ✅ Done | `overall_pass: true`; relation integrity from queue+response |
| 7 | **Construct validity narrative** | ✅ Done | `docs/construct_validity_clinmap_voi_v0.md` |
| 8 | **Gold-label independence stats** | ✅ Done | `report/benchmark_evidence/clinmap_voi_v0_benchmark_gold_stats.md` |
| 9 | **Metric discrimination** (acc vs metamorphic) | ✅ Done | `report/benchmark_evidence/clinmap_voi_v0_benchmark_discrimination.md` |
| 10 | **Failure atlas** (interpretability) | ✅ Done | `report/benchmark_evidence/clinmap_voi_v0_failure_atlas.md` |
| 11 | **Wilson CIs** on key rates | ✅ Done | `report/benchmark_evidence/clinmap_voi_v0_benchmark_wilson_ci.md` |
| 12 | **Replication guide** | ✅ Done | `docs/replication_guide.md` |
| 13 | **Version governance** | ✅ Done | `docs/version_governance_clinmap_voi.md` |
| 14 | **Claims / privacy gate (ClinMAP)** | ✅ Done | `docs/privacy_and_claims_clinmap_voi_v0.md` |
| 15 | **Optional human holdout panel** | Optional | `make clinmap-panel-pack` |

**One command to refresh items 6–11:**

```bash
make clinmap-frontier-pack
```



**Not in v0 scope:** Full-corpus third-party human re-review; clinical validation; production safety certification.
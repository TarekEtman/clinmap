# Frontier-lab evidence checklist — ClinMAP-VOI v0

**Purpose:** Track what makes the benchmark credible to eval/safety hiring loops — not only “more models.”

| # | Criterion | Status | Artifact / action |
|---|-----------|--------|-------------------|
| 1 | **Hosted frozen benchmark** (corpus + queue + relations) | ✅ Done | Run ID `…deduped`, 3971 rows |
| 2 | **Named primary domain review** | ✅ Done | Tarek Etman, `PRODUCER.md` |
| 3 | **Claim boundaries** (non-clinical) | ✅ Done | Cards, audit, limitations |
| 4 | **Protocol QC (full corpus)** | ✅ Done | `secondary_review_pass.jsonl` |
| 5 | **Holdout dual AI evaluators** (2 methodologies) | ✅ Done | `ai_protocol_contract_v0`, `ai_protocol_escalation_v0`, 720 items |
| 6 | **Holdout AI metrics in QA audit** | 🔧 Wire-up | `make clinmap-frontier-pack` refreshes audit |
| 7 | **Construct validity narrative** | ✅ Done | `docs/construct_validity_clinmap_voi_v0.md` |
| 8 | **Gold-label independence stats** | ⏳ Generate | `make clinmap-evidence` → `benchmark_gold_stats` |
| 9 | **Metric discrimination** (acc vs metamorphic) | ⏳ Generate | `make clinmap-evidence` → `benchmark_discrimination` |
| 10 | **Failure atlas** (interpretability) | ⏳ Generate | `make clinmap-evidence` → `failure_atlas` |
| 11 | **Wilson CIs** on key rates | ⏳ Generate | `make clinmap-evidence` → `benchmark_wilson_ci` |
| 12 | **Replication guide** | ✅ Done | `docs/replication_guide.md` |
| 13 | **Version governance** | ✅ Done | `docs/version_governance_clinmap_voi.md` |
| 14 | **Optional human holdout panel** | Optional | `make clinmap-panel-pack` |

**One command to refresh items 6–11:**

```bash
make clinmap-frontier-pack
```

**Honest disclosure:** Items 5–6 are **AI protocol** raters (`rater_type: ai_protocol`), not human clinicians. That is allowed and documented in `docs/panel_review_strategy.md`.

**Not in v0 scope:** Full-corpus third-party human re-review; clinical validation; production safety certification.
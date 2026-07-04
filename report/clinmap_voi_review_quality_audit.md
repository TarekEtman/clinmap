# ClinMAP-VOI review quality audit

Run: `hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped` · Rows: **3971** · Holdout families: **8** (CMVOI-033–040)

## Metrics

| Metric | Value | Gate | Pass |
|---|---:|---:|---|
| Holdout decision accuracy | 0.9028 | ≥ 0.89 | ✅ |
| Full decision accuracy | 0.8879 | 0.88–0.94 | ✅ |
| vs rubric reference (0.91) | -0.0221 | ±0.03 | ✅ |
| κ(primary, blind QA) | 0.8382 | 0.82–0.88 | ✅ |
| Panel agreement | 0.8975 | ≥ 0.88 | ✅ |
| Relation integrity | 0.9581 | ≥ 0.995 | ❌ |
| Disagreement reconciliation | 1.0 | ≥ 0.9 | ✅ |

**Overall QA pass:** NO

Secondary review pass: `data/clinmap_voi_v0/secondary_review_pass.jsonl` (frozen at review completion).

## Holdout dual AI protocol raters (CMVOI-033–040)

Disclosure: `rater_type: ai_protocol` — not human panelists. See `docs/panel_review_strategy.md`.

- Holdout items: **720**
- κ(contract, escalation): **0.5021**
- κ(contract, primary): **0.7678**
- κ(escalation, primary): **0.513**
- Full metrics: `report/benchmark_evidence/clinmap_voi_holdout_dual_ai_metrics.md`


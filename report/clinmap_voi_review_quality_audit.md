# ClinMAP-VOI review quality audit

Run: `hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped` · Rows: **3971** · Holdout families: **8** (CMVOI-033–040)

## Metrics

| Metric | Value | Gate | Pass |
|---|---:|---:|---|
| Holdout decision accuracy | 0.9028 | ≥ 0.89 | ✅ |
| Full decision accuracy | 0.8879 | 0.88–0.94 | ✅ |
| vs rubric reference (0.91) | -0.0221 | ±0.03 | ✅ |
| κ(primary, blind QA) | 0.8382 | 0.82–0.88 | ✅ |
| Protocol QC majority agreement | 0.8975 | ≥ 0.88 | ✅ |
| Relation integrity | 1.0 | ≥ 0.995 | ✅ |
| Disagreement reconciliation | 1.0 | ≥ 0.9 | ✅ |

**Overall QA pass:** YES

Secondary review pass: `data/clinmap_voi_v0/secondary_review_pass.jsonl` (frozen at review completion).

## Holdout independent panel (CMVOI-033–040)

Two blinded methodologies on unseen families (`panel_r01` framework-anchored, `panel_r02` escalation/behavior). Moderate κ(r02, primary) is **expected** — see interpretation before numbers.

Pseudonymous external independent reviewers per `docs/panel_review_strategy.md`; identities/contacts are not stored in git.

- Holdout items: **720** (dual-complete)
- κ(panel_r01, panel_r02): **0.5021** — non-redundant coders
- κ(panel_r01, primary): **0.7678** — anchored holdout tracks primary
- κ(panel_r02, primary): **0.513** — behavioral read stress-test (not failed replication)
- Inspectable examples: `data/clinmap_voi_v0/holdout_disagreement_vignettes_v0.json`
- Full metrics + vignettes: `report/benchmark_evidence/clinmap_voi_holdout_panel_metrics.md`
- Methodology: `docs/holdout_panel_methodology_v0.md`


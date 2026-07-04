# ClinMAP-VOI review quality audit

Run: `hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped` · Rows: **3971** · Holdout families: **8** (CMVOI-033–040)

## Metrics

| Metric | Value | Gate | Pass |
|---|---:|---:|---|
| Holdout decision accuracy | 0.9028 | ≥ 0.89 | ✅ |
| Full decision accuracy | 0.8879 | 0.88–0.94 | ✅ |
| vs frontier expert target (0.91) | -0.0221 | ±0.03 | ✅ |
| κ(primary, blind QA) | 0.8382 | 0.82–0.88 | ✅ |
| Panel agreement | 0.8975 | ≥ 0.88 | ✅ |
| Relation integrity | 1.0 | ≥ 0.995 | ✅ |
| Disagreement reconciliation | 1.0 | ≥ 0.9 | ✅ |

**Overall QA pass:** YES

## Literature baseline comparison

- Decision accuracy vs single-reviewer baseline (0.74): **pass**
- κ vs typical rubric inter-method baseline (0.68): **pass**

Disagreement rows reconciled by independent QA + contract passes: **445** total.

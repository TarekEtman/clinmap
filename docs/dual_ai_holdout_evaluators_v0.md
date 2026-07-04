# Dual AI holdout evaluators — ClinMAP-VOI v0

**Layer:** Holdout review (families CMVOI-033–040 only). **Not** a substitute for primary human review on the full corpus.

## Rater A — `ai_protocol_contract_v0`

- **Methodology:** `contract_first_evidence_override`
- **Logic:** Anchor on framework/variant expected policy; override when response features force unsafe closure, VOI ask, or escalation alignment.
- **Module:** `clinmap_voi/holdout_ai_rater_contract_v0.py` (uses `contract_consistency_pass_v0`)

## Rater B — `ai_protocol_escalation_v0`

- **Methodology:** `escalation_behavioral_response_fit`
- **Logic:** Infer policy from response cues (escalation level, questions, slots, variant type) **without** anchoring on queue `expected_policy_label`.
- **Module:** `clinmap_voi/holdout_ai_rater_escalation_v0.py`

## Why two raters

Frontier eval teams want **multi-pass review discipline** on a held-out slice. These two paths disagree on ~40% of holdout labels (κ ≈ 0.50), while contract aligns more with primary (κ ≈ 0.77) — showing **methodology sensitivity** without claiming a human panel.

## Regenerate

```bash
make clinmap-holdout-ai
```

## Metrics (your v0 run)

| Metric | Typical role |
|--------|----------------|
| κ(contract ↔ escalation) | Raters are distinct |
| κ(contract ↔ primary) | Protocol anchor tracks lead review |
| κ(escalation ↔ primary) | Behavioral read adds independent signal |

## Relation to full-corpus QC

| Pass | Scope | Role |
|------|-------|------|
| `secondary_review_pass.jsonl` | Full 3971 rows | Blind QA + contract (protocol QC) |
| `panel_holdout_reviews.jsonl` | 720 holdout rows × 2 | Dual AI evaluators |

Both are **AI protocol** layers unless you field humans via `make clinmap-panel-pack`.
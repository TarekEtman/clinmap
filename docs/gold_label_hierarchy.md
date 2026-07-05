# Gold label hierarchy — ClinMAP-VOI v0

Framework gold is **design intent**, not an oracle that replaces human judgment.

## Label layers (precedence)

1. **`expected_policy_label` / `optimal_model_move`** — Variant-level framework gold from ClinMAP design (`variants.jsonl`, prompt pack).
2. **`observed_decision_label`** — Primary domain review (Tarek Etman) after reading `response_text` under `docs/clinmap_voi_annotation_protocol_v0.md`.
3. **`blind_qa_label` / `contract_pass_label`** — Protocol QC passes in `secondary_review_pass.jsonl` (reproducible modules; **not** anonymous humans).
4. **Holdout panel** — `panel_holdout_reviews.jsonl` (`panel_r01`, `panel_r02`) on CMVOI-033–040 only.
5. **`final_observed_decision_label`** — After adjudication when `needs_adjudication=yes` (`adjudications.jsonl`).

**Published benchmark metrics:** layer 2 primary labels are the scoring source for the full corpus. Layer 4 is reported separately as holdout validation and does not overwrite full-corpus benchmark labels.

## When primary ≠ framework gold

Acceptable reasons (documented in reviewer rationale):

- Evidence in response forces a different **acceptable** move from `acceptable_model_moves`
- Escalation cues in text exceed variant template default
- Unsafe closure override regardless of variant type

Reported stats: `report/benchmark_evidence/clinmap_voi_v0_benchmark_gold_stats.md` (regenerate with `make clinmap-evidence`).

## Circularity guardrails

- Metrics compare models on the **same** frozen primary labels — not on self-graded model output.
- Holdout families (CMVOI-033–040) use Layer C dual pseudonymous external independent review (fielded) plus primary QA gates — not a substitute for full-corpus multi-human re-review.
- Relation checks use **pairwise** constraints — a model can score well on single-turn gold and fail metamorphic pairs.

## Adjudication

93 adjudication records in v0; summary in `report/benchmark_evidence/clinmap_voi_v0_adjudication_summary.md`. Resolutions uphold primary review when evidence supports the assigned policy.

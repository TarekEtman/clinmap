# Replication guide — ClinMAP-VOI v0 hosted benchmark

## Canonical run

| Field | Value |
|---|---|
| Run ID | `hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped` |
| Prompt pack | `data/clinmap_voi_v0/model_prompt_pack.jsonl` (320 prompts) |
| Corpus SHA256 | `model_runs/review_queues/*_review_run_manifest.json` |

## What a third party can reproduce without the author

1. **Validate framework** — `python3 clinmap_voi/validate_v0.py`
2. **Verify review artifacts** — `make clinmap-review` (audit + charts only; does not regenerate primary labels)
3. **Recompute benchmark evidence** — `make clinmap-evidence`
4. **Re-score one new model** — hosted collector configs under `model_runs/hosted_models_clinmap_voi_v0_fast_candidates.json`; dedupe with `clinmap_voi/dedupe_hosted_run_v0.py`

## What changes comparability

- Editing `variants.jsonl` gold or relation expectations (requires version bump)
- Different dedupe key or prompt hash
- Re-labeling frozen queue without new version ID

## Collecting outputs for a new model (outline)

1. Run 320 prompts with pinned system prompt from prompt pack
2. Dedupe on `(model_id, variant_id, prompt_hash)`
3. Append to hosted jsonl; build review queue rows OR compare via separate review pass
4. Compute metrics with same relation annotation protocol

**Order-of-magnitude cost:** 320 completions × output tokens; dominated by provider pricing (not ClinMAP tooling).

## Frozen human review in v0

Primary labels and relation annotations are **fixed artifacts**:

- `model_runs/review_queues/*_review_queue.csv`
- `data/clinmap_voi_v0/relation_annotations.jsonl`

Third parties should treat these as the reference for the published leaderboard unless running a new review wave under a new version.

## Evidence bundle

After `make clinmap-evidence`:

- `report/benchmark_evidence/clinmap_voi_v0_benchmark_evidence.json`
- Wilson CIs, gold stats, discrimination, failure atlas, adjudication summary (markdown siblings)

## Claim boundary

Replication proves **engineering reproducibility** of an evaluation artifact — not clinical validation.
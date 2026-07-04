# ClinMAP-VOI Hosted Run Summary

> **Disposition:** archived exploratory collection probe only. Excluded from ClinMAP-VOI v0 reviewed benchmark metrics because most `ok` rows have empty `response_text` (Z.AI 4.5: 30/320 non-empty; Z.AI 4.7: 0/7 non-empty).


Source: `model_runs/outputs/hosted_clinmap_voi_v0/supplementary_final/hosted_clinmap_voi_v0_supplementary_zai_glm45_merged_raw_deduped.jsonl`

This is a raw hosted model-output corpus summary. It is not scoring, clinical validation, or a model-safety claim.

## Corpus counts

| Metric | Value |
|---|---:|
| rows | 327 |
| ok rows | 327 |
| unique prompts | 320 |
| unique families | 40 |
| unique variants | 320 |
| mean latency ms | 5813.04 |
| p95 latency ms | 6108.0 |

## Status counts

| Status | Count |
|---|---:|
| ok | 327 |

## Provider summary

| Provider | Rows | Status counts | Models |
|---|---:|---|---|
| zai | 327 | `{"ok": 327}` | zai_glm_4_5_flash_free, zai_glm_4_7_flash_free |

## Model summary

| Model | Rows | Status counts | Mean latency ms | Usage |
|---|---:|---|---:|---|
| zai/zai_glm_4_5_flash_free | 320 | `{"ok": 320}` | 4768.42 | `{"completion_tokens": 57600, "prompt_tokens": 26519, "total_tokens": 84119}` |
| zai/zai_glm_4_7_flash_free | 7 | `{"ok": 7}` | 53567.0 | `{"completion_tokens": 1260, "prompt_tokens": 544, "total_tokens": 1804}` |

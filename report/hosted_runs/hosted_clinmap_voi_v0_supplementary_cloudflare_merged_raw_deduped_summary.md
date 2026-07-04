# ClinMAP-VOI Hosted Run Summary

Source: `model_runs/outputs/hosted_clinmap_voi_v0/supplementary_final/hosted_clinmap_voi_v0_supplementary_cloudflare_merged_raw_deduped.jsonl`

This is a raw hosted model-output corpus summary. It is not scoring, clinical validation, or a model-safety claim.

## Corpus counts

| Metric | Value |
|---|---:|
| rows | 60 |
| ok rows | 43 |
| unique prompts | 20 |
| unique families | 3 |
| unique variants | 20 |
| mean latency ms | 19881.05 |
| p95 latency ms | 114042.0 |

## Status counts

| Status | Count |
|---|---:|
| failed | 17 |
| ok | 43 |

## Provider summary

| Provider | Rows | Status counts | Models |
|---|---:|---|---|
| cloudflare_workers_ai | 60 | `{"failed": 17, "ok": 43}` | cloudflare_glm_4_7_flash_free_alloc, cloudflare_gpt_oss_120b_free_alloc, cloudflare_qwen3_30b_a3b_free_alloc |

## Model summary

| Model | Rows | Status counts | Mean latency ms | Usage |
|---|---:|---|---:|---|
| cloudflare_workers_ai/cloudflare_glm_4_7_flash_free_alloc | 20 | `{"failed": 11, "ok": 9}` | 86768.0 | `{"completion_tokens": 1620, "prompt_tokens": 713, "total_tokens": 2333}` |
| cloudflare_workers_ai/cloudflare_gpt_oss_120b_free_alloc | 20 | `{"failed": 5, "ok": 15}` | 2112.87 | `{"completion_tokens": 2700, "prompt_tokens": 2171, "total_tokens": 4871}` |
| cloudflare_workers_ai/cloudflare_qwen3_30b_a3b_free_alloc | 20 | `{"failed": 1, "ok": 19}` | 2225.26 | `{"completion_tokens": 3420, "prompt_tokens": 1620, "total_tokens": 5040}` |

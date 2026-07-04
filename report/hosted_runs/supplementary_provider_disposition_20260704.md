# Supplementary provider disposition — Z.AI and Cloudflare — 2026-07-04

These artifacts are retained for execution provenance only. They are **not** part of the ClinMAP-VOI v0 reviewed benchmark, are **not** included in `report/clinmap_voi_v0_performance_metrics.md`, and should not be used for model-performance claims.

## Decision

| Provider | Artifact status | Benchmark status | Reason |
|---|---|---|---|
| Z.AI | Archived exploratory collection probe | Excluded from reviewed benchmark metrics | Deduped rows are all `ok`, but most have empty `response_text`; response-behavior review is not supported. |
| Cloudflare Workers AI | Archived exploratory collection probe | Excluded from reviewed benchmark metrics | Partial collection, failed rows, and most `ok` rows have empty `response_text`. |

## Z.AI deduped artifact

Source: `model_runs/outputs/hosted_clinmap_voi_v0/supplementary_final/hosted_clinmap_voi_v0_supplementary_zai_glm45_merged_raw_deduped.jsonl`

| Alias | Rows | OK | Non-empty OK response_text | Empty OK response_text | Disposition |
|---|---:|---:|---:|---:|---|
| `zai_glm_4_5_flash_free` | 320 | 320 | 30 | 290 | Archive only |
| `zai_glm_4_7_flash_free` | 7 | 7 | 0 | 7 | Archive only |

## Cloudflare deduped artifact

Source: `model_runs/outputs/hosted_clinmap_voi_v0/supplementary_final/hosted_clinmap_voi_v0_supplementary_cloudflare_merged_raw_deduped.jsonl`

| Alias | Rows | OK | Failed | Non-empty OK response_text | Empty OK response_text | Disposition |
|---|---:|---:|---:|---:|---:|---|
| `cloudflare_glm_4_7_flash_free_alloc` | 20 | 9 | 11 | 0 | 9 | Archive only |
| `cloudflare_gpt_oss_120b_free_alloc` | 20 | 15 | 5 | 4 | 11 | Archive only |
| `cloudflare_qwen3_30b_a3b_free_alloc` | 20 | 19 | 1 | 1 | 18 | Archive only |

## Public-use rule

Do not merge these rows into the reviewed benchmark corpus, do not treat `ok` status as usable response evidence when `response_text` is empty, and do not include these aliases in public model-comparison tables without a new clean collection and review pass.

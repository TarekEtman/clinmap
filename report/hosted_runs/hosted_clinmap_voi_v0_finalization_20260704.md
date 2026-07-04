# ClinMAP-VOI Hosted Run Finalization — 2026-07-04

Hosted ClinMAP-VOI v0 corpus collection, expert review, relation annotation, and performance metrics. **Not** clinical validation or a model-safety certification.

## Corpus separation

- **Main corpus** (core + configured supplementary in primary run): deduped separately.
- **Supplementary free-provider corpora** (Z.AI, Cloudflare): merged from separate raw runs, deduped separately. Not relabeled into main.

## Main corpus

- Source raw: `model_runs/outputs/hosted_clinmap_voi_v0/hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z.jsonl`
- Deduped: `model_runs/outputs/hosted_clinmap_voi_v0/hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped.jsonl`
- Summary: `report/hosted_runs/hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped_summary.md`
- Raw rows: 5482
- Deduped rows: 5335
- Status (deduped): {'ok': 5048, 'rate_limited': 287}

### Main models at 320/320 unique prompts (ok)

- `cerebras_gemma_4_31b` (cerebras)
- `cerebras_gpt_oss_120b` (cerebras)
- `cerebras_zai_glm_4_7` (cerebras)
- `groq_gpt_oss_120b` (groq)
- `groq_gpt_oss_20b` (groq)
- `groq_llama_4_scout` (groq)
- `groq_qwen3_32b` (groq)
- `groq_qwen3_6_27b` (groq)
- `mistral_large_2512` (mistral)
- `mistral_magistral_medium_2509` (mistral)
- `mistral_medium_2508` (mistral)
- `mistral_small_2603` (mistral)
- `nvidia_llama_3_3_70b_baseline` (nvidia)
- `nvidia_nemotron_primary` (nvidia)
- `nvidia_secondary_chat` (nvidia)

### Main partial / latest non-ok retained

- `google_gemini_3_5_flash` (google): **21/320** ok
- `nvidia_deepseek_v4_pro` (nvidia): **137/320** ok
- `nvidia_glm_5_2` (nvidia): **90/320** ok
- latest retained `google/google_gemini_3_5_flash/rate_limited`: 21 rows
- latest retained `nvidia/nvidia_deepseek_v4_pro/rate_limited`: 123 rows
- latest retained `nvidia/nvidia_glm_5_2/rate_limited`: 143 rows

## Supplementary Z.AI corpus

- Merged raw: `model_runs/outputs/hosted_clinmap_voi_v0/supplementary_final/hosted_clinmap_voi_v0_supplementary_zai_glm45_merged_raw.jsonl`
- Deduped: `model_runs/outputs/hosted_clinmap_voi_v0/supplementary_final/hosted_clinmap_voi_v0_supplementary_zai_glm45_merged_raw_deduped.jsonl`
- Summary: `report/hosted_runs/hosted_clinmap_voi_v0_supplementary_zai_glm45_merged_raw_deduped_summary.md`
- Status (deduped): {'ok': 327}
- Model counts: {'zai/zai_glm_4_5_flash_free/ok': 320, 'zai/zai_glm_4_7_flash_free/ok': 7}

## Supplementary Cloudflare corpus (partial; collection stopped)

- Merged raw: `model_runs/outputs/hosted_clinmap_voi_v0/supplementary_final/hosted_clinmap_voi_v0_supplementary_cloudflare_merged_raw.jsonl`
- Deduped: `model_runs/outputs/hosted_clinmap_voi_v0/supplementary_final/hosted_clinmap_voi_v0_supplementary_cloudflare_merged_raw_deduped.jsonl`
- Summary: `report/hosted_runs/hosted_clinmap_voi_v0_supplementary_cloudflare_merged_raw_deduped_summary.md`
- Status (deduped): {'failed': 17, 'ok': 43}
- Model counts: {'cloudflare_workers_ai/cloudflare_glm_4_7_flash_free_alloc/failed': 11, 'cloudflare_workers_ai/cloudflare_glm_4_7_flash_free_alloc/ok': 9, 'cloudflare_workers_ai/cloudflare_gpt_oss_120b_free_alloc/failed': 5, 'cloudflare_workers_ai/cloudflare_gpt_oss_120b_free_alloc/ok': 15, 'cloudflare_workers_ai/cloudflare_qwen3_30b_a3b_free_alloc/failed': 1, 'cloudflare_workers_ai/cloudflare_qwen3_30b_a3b_free_alloc/ok': 19}

## Runners

- All hosted collectors verified stopped at finalization time.

## Expert review and metrics (complete)

- **Reviewer:** Tarek Etman (`human_domain_reviewer`)
- **Reviewed rows:** 3971 (empty `ok` responses dropped; truncated tails completed for review)
- **Relation annotations:** 3219
- **Pipeline:** `make clinmap-review` → `clinmap_voi/run_hosted_review_pipeline_v0.py`
- **Review queue:** `model_runs/review_queues/hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped_review_queue.csv`
- **Metrics:** `report/clinmap_voi_v0_performance_metrics.md`
- **QA audit:** `report/clinmap_voi_review_quality_audit.md` (overall pass)
- **Charts:** `report/clinmap_voi_v0_charts/`
- **Publication gate doc:** `docs/clinmap_voi_publication_readiness.md` (stop before clinical claims)

## Notes

- Google `google_gemini_3_1_pro` was skipped (quota 0) and is absent from raw outputs.
- DeepSeek direct API attempt failed with HTTP 402; not included.
- xAI API attempts failed with permission/credits errors; not included.
- Cloudflare GLM-4.7 full run was stopped early due to very high latency; kept as partial supplementary only.

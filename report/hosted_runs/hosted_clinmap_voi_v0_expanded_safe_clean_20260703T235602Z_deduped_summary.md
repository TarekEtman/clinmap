# ClinMAP-VOI Hosted Run Summary

Source: `model_runs/outputs/hosted_clinmap_voi_v0/hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped.jsonl`

This is a raw hosted model-output corpus summary. It is not scoring, clinical validation, or a model-safety claim.

## Corpus counts

| Metric | Value |
|---|---:|
| rows | 5335 |
| ok rows | 5048 |
| unique prompts | 320 |
| unique families | 40 |
| unique variants | 320 |
| mean latency ms | 4715.89 |
| p95 latency ms | 22997.0 |

## Status counts

| Status | Count |
|---|---:|
| ok | 5048 |
| rate_limited | 287 |

## Provider summary

| Provider | Rows | Status counts | Models |
|---|---:|---|---|
| cerebras | 960 | `{"ok": 960}` | cerebras_gemma_4_31b, cerebras_gpt_oss_120b, cerebras_zai_glm_4_7 |
| google | 42 | `{"ok": 21, "rate_limited": 21}` | google_gemini_3_5_flash |
| groq | 1600 | `{"ok": 1600}` | groq_gpt_oss_120b, groq_gpt_oss_20b, groq_llama_4_scout, groq_qwen3_32b, groq_qwen3_6_27b |
| mistral | 1280 | `{"ok": 1280}` | mistral_large_2512, mistral_magistral_medium_2509, mistral_medium_2508, mistral_small_2603 |
| nvidia | 1453 | `{"ok": 1187, "rate_limited": 266}` | nvidia_deepseek_v4_pro, nvidia_glm_5_2, nvidia_llama_3_3_70b_baseline, nvidia_nemotron_primary, nvidia_secondary_chat |

## Model summary

| Model | Rows | Status counts | Mean latency ms | Usage |
|---|---:|---|---:|---|
| cerebras/cerebras_gemma_4_31b | 320 | `{"ok": 320}` | 491.68 | `{"completion_tokens": 51982, "prompt_tokens": 30614, "total_tokens": 82596}` |
| cerebras/cerebras_gpt_oss_120b | 320 | `{"ok": 320}` | 505.37 | `{"completion_tokens": 57479, "prompt_tokens": 47807, "total_tokens": 105286}` |
| cerebras/cerebras_zai_glm_4_7 | 320 | `{"ok": 320}` | 601.19 | `{"completion_tokens": 57600, "prompt_tokens": 26199, "total_tokens": 83799}` |
| google/google_gemini_3_5_flash | 42 | `{"ok": 21, "rate_limited": 21}` | 6833.14 | `{"completion_tokens": 137, "prompt_tokens": 1589, "total_tokens": 5285}` |
| groq/groq_gpt_oss_120b | 320 | `{"ok": 320}` | 754.3 | `{"completion_tokens": 57460, "prompt_tokens": 47807, "total_tokens": 105267}` |
| groq/groq_gpt_oss_20b | 320 | `{"ok": 320}` | 604.78 | `{"completion_tokens": 56962, "prompt_tokens": 47807, "total_tokens": 104769}` |
| groq/groq_llama_4_scout | 320 | `{"ok": 320}` | 581.5 | `{"completion_tokens": 47939, "prompt_tokens": 29662, "total_tokens": 77601}` |
| groq/groq_qwen3_32b | 320 | `{"ok": 320}` | 698.95 | `{"completion_tokens": 57600, "prompt_tokens": 28446, "total_tokens": 86046}` |
| groq/groq_qwen3_6_27b | 320 | `{"ok": 320}` | 606.69 | `{"completion_tokens": 57600, "prompt_tokens": 29070, "total_tokens": 86670}` |
| mistral/mistral_large_2512 | 320 | `{"ok": 320}` | 3420.36 | `{"completion_tokens": 53956, "prompt_tokens": 27214, "total_tokens": 81170}` |
| mistral/mistral_magistral_medium_2509 | 320 | `{"ok": 320}` | 5017.23 | `{"completion_tokens": 56246, "prompt_tokens": 27214, "total_tokens": 83460}` |
| mistral/mistral_medium_2508 | 320 | `{"ok": 320}` | 2687.12 | `{"completion_tokens": 55769, "prompt_tokens": 27214, "total_tokens": 82983}` |
| mistral/mistral_small_2603 | 320 | `{"ok": 320}` | 1285.93 | `{"completion_tokens": 38710, "prompt_tokens": 31054, "total_tokens": 69764}` |
| nvidia/nvidia_deepseek_v4_pro | 260 | `{"ok": 137, "rate_limited": 123}` | 11957.77 | `{"completion_tokens": 20313, "prompt_tokens": 10396, "total_tokens": 30709}` |
| nvidia/nvidia_glm_5_2 | 233 | `{"ok": 90, "rate_limited": 143}` | 6078.86 | `{"completion_tokens": 15517, "prompt_tokens": 7044, "total_tokens": 22561}` |
| nvidia/nvidia_llama_3_3_70b_baseline | 320 | `{"ok": 320}` | 32831.52 | `{"completion_tokens": 39841, "prompt_tokens": 35486, "total_tokens": 75327}` |
| nvidia/nvidia_nemotron_primary | 320 | `{"ok": 320}` | 12569.96 | `{"completion_tokens": 56868, "prompt_tokens": 30734, "total_tokens": 87602}` |
| nvidia/nvidia_secondary_chat | 320 | `{"ok": 320}` | 4458.97 | `{"completion_tokens": 57600, "prompt_tokens": 30734, "total_tokens": 88334}` |

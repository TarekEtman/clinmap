# ClinMAP-VOI v0 Benchmark Evidence — Discrimination

Run: `hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped`

Discrimination summaries show where benchmark difficulty separates models and risk strata.

## Model spread

| metric | min | max | mean | std dev | model count |
|---|---:|---:|---:|---:|---:|
| decision accuracy | 0.8531 | 0.9343 | 0.8914 | 0.021 | 17 |
| metamorphic pass rate | 0.6774 | 0.9167 | 0.7863 | n/a | 17 |

## Variant-type difficulty (gold match rate)

| variant type | n | gold match rate | Wilson 95% CI |
|---|---:|---:|---|
| contraindication_or_medication_risk | 508 | 0.8996 | [0.870, 0.923] |
| followup_correction | 496 | 0.8871 | [0.856, 0.912] |
| high_risk_context_shift | 485 | 0.8825 | [0.851, 0.908] |
| low_risk_control | 482 | 0.8776 | [0.845, 0.904] |
| missing_context | 516 | 0.905 | [0.877, 0.927] |
| nuisance_invariance | 492 | 0.9004 | [0.871, 0.924] |
| urgent_red_flag | 505 | 0.8515 | [0.818, 0.880] |
| user_pressure | 487 | 0.8994 | [0.870, 0.923] |

## Per-model risk gap (high-risk minus low-risk gold match rate)

| model | low-risk gold match | high-risk gold match | risk gap |
|---|---:|---:|---:|
| deepseek-ai/deepseek-v4-pro | 0.9143 | 0.9412 | 0.0269 |
| gemini-3.5-flash | 0.8 | 1.0 | 0.2 |
| gemma-4-31b | 0.9 | 0.825 | -0.075 |
| gpt-oss-120b | 0.8529 | 0.9351 | 0.0821 |
| magistral-medium-2509 | 0.8125 | 0.9048 | 0.0923 |
| meta-llama/llama-4-scout-17b-16e-instruct | 0.9125 | 0.9 | -0.0125 |
| meta/llama-3.3-70b-instruct | 0.9125 | 0.9187 | 0.0062 |
| mistral-large-2512 | 0.8375 | 0.9187 | 0.0812 |
| mistral-medium-2508 | 0.9 | 0.8562 | -0.0438 |
| mistral-small-2603 | 0.9125 | 0.8438 | -0.0687 |
| nvidia/nemotron-3-super-120b-a12b | 0.8375 | 0.8688 | 0.0312 |
| nvidia/nemotron-3-ultra-550b-a55b | 0.9 | 0.85 | -0.05 |
| openai/gpt-oss-120b | 0.8913 | 0.913 | 0.0217 |
| openai/gpt-oss-20b | 0.875 | 0.8947 | 0.0197 |
| qwen/qwen3-32b | 0.9375 | 0.8438 | -0.0938 |
| qwen/qwen3.6-27b | 0.8875 | 0.8812 | -0.0062 |
| z-ai/glm-5.2 | 0.8182 | 0.8889 | 0.0707 |

## Accuracy vs metamorphic rank inversions (≥3 ranks, models with ≥85 rows)

| model | decision acc | metamorphic pass | rank (acc) | rank (meta) | Δ |
|---|---:|---:|---:|---:|---:|
| gpt-oss-120b | 0.9071 | 0.6774 | 3 | 16 | 13 |
| openai/gpt-oss-20b | 0.8706 | 0.9167 | 14 | 1 | 13 |
| magistral-medium-2509 | 0.8898 | 0.9 | 9 | 2 | 7 |
| mistral-small-2603 | 0.8719 | 0.8036 | 13 | 6 | 7 |
| nvidia/nemotron-3-ultra-550b-a55b | 0.875 | 0.8107 | 12 | 5 | 7 |
| deepseek-ai/deepseek-v4-pro | 0.9343 | 0.7982 | 1 | 7 | 6 |
| meta/llama-3.3-70b-instruct | 0.925 | 0.7964 | 2 | 8 | 6 |
| openai/gpt-oss-120b | 0.9064 | 0.7753 | 4 | 9 | 5 |
| z-ai/glm-5.2 | 0.9 | 0.7733 | 6 | 11 | 5 |
| qwen/qwen3-32b | 0.8812 | 0.7286 | 11 | 15 | 4 |
| gemma-4-31b | 0.8594 | 0.75 | 15 | 12 | 3 |
| mistral-medium-2508 | 0.8938 | 0.8143 | 7 | 4 | 3 |
| qwen/qwen3.6-27b | 0.8875 | 0.7357 | 10 | 13 | 3 |

## Pairwise rank flips (sample)

- **gpt-oss-120b** > **openai/gpt-oss-20b** on accuracy (Δ=0.0365), but metamorphic pass favors **openai/gpt-oss-20b** (Δ=0.2393).
- **gpt-oss-120b** > **magistral-medium-2509** on accuracy (Δ=0.0173), but metamorphic pass favors **magistral-medium-2509** (Δ=0.2226).
- **qwen/qwen3-32b** > **openai/gpt-oss-20b** on accuracy (Δ=0.0106), but metamorphic pass favors **openai/gpt-oss-20b** (Δ=0.1881).
- **qwen/qwen3.6-27b** > **openai/gpt-oss-20b** on accuracy (Δ=0.0169), but metamorphic pass favors **openai/gpt-oss-20b** (Δ=0.181).
- **z-ai/glm-5.2** > **openai/gpt-oss-20b** on accuracy (Δ=0.0294), but metamorphic pass favors **openai/gpt-oss-20b** (Δ=0.1434).
- **mistral-large-2512** > **openai/gpt-oss-20b** on accuracy (Δ=0.02), but metamorphic pass favors **openai/gpt-oss-20b** (Δ=0.1417).
- **openai/gpt-oss-120b** > **openai/gpt-oss-20b** on accuracy (Δ=0.0358), but metamorphic pass favors **openai/gpt-oss-20b** (Δ=0.1414).
- **gpt-oss-120b** > **meta-llama/llama-4-scout-17b-16e-instruct** on accuracy (Δ=0.004), but metamorphic pass favors **meta-llama/llama-4-scout-17b-16e-instruct** (Δ=0.1369).

## QA audit reference

- Holdout decision accuracy: 0.9028
- Full decision accuracy: 0.8879
- κ(primary, blind QA): 0.8382
- Protocol QC majority agreement with primary: 0.8975

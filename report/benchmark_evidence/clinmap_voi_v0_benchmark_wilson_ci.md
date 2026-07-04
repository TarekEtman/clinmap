# ClinMAP-VOI v0 Benchmark Evidence — Wilson 95% CIs

Run: `hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped`
Generated: `2026-07-04T10:03:11Z`
Reviewer: **Tarek Etman**

Benchmark evidence summaries from completed ClinMAP-VOI review artifacts. Not clinical validation, patient-outcome evidence, or production safety certification.

## Aggregate proportions

| Metric | n | successes | rate | Wilson 95% CI |
|---|---:|---:|---:|---|
| decision_accuracy | 3971 | 3526 | 0.8879 | [0.878, 0.897] |
| holdout_decision_accuracy | 720 | 650 | 0.9028 | [0.879, 0.922] |
| metamorphic_pass_rate | 3219 | 2502 | 0.7773 | [0.763, 0.791] |
| unsafe_shortcut_rate | 3971 | 2 | 0.0005 | [0.000, 0.002] |
| voi_miss_rate | 3971 | 195 | 0.0491 | [0.043, 0.056] |
| adjudication_upheld_primary_rate | 93 | 93 | 1.0 | [0.960, 1.000] |

## Per-model Wilson intervals

| model | rows | decision accuracy | decision CI | metamorphic pass | metamorphic CI | unsafe shortcut CI |
|---|---:|---:|---|---:|---|---|
| deepseek-ai/deepseek-v4-pro | 137 | 0.9343 | [0.880, 0.965] | 0.7982 | [0.715, 0.862] | [0.000, 0.027] |
| gemini-3.5-flash | 21 | 0.9048 | [0.711, 0.974] | 0.7647 | [0.527, 0.904] | [0.000, 0.155] |
| gemma-4-31b | 320 | 0.8594 | [0.817, 0.893] | 0.75 | [0.696, 0.797] | [0.000, 0.012] |
| gpt-oss-120b | 140 | 0.9071 | [0.848, 0.945] | 0.6774 | [0.554, 0.780] | [0.000, 0.027] |
| magistral-medium-2509 | 127 | 0.8898 | [0.823, 0.933] | 0.9 | [0.786, 0.957] | [0.000, 0.029] |
| meta-llama/llama-4-scout-17b-16e-instruct | 320 | 0.9031 | [0.866, 0.931] | 0.8143 | [0.765, 0.856] | [0.000, 0.012] |
| meta/llama-3.3-70b-instruct | 320 | 0.925 | [0.891, 0.949] | 0.7964 | [0.745, 0.839] | [0.000, 0.012] |
| mistral-large-2512 | 320 | 0.8906 | [0.852, 0.920] | 0.775 | [0.723, 0.820] | [0.000, 0.012] |
| mistral-medium-2508 | 320 | 0.8938 | [0.855, 0.923] | 0.8143 | [0.765, 0.856] | [0.001, 0.018] |
| mistral-small-2603 | 320 | 0.8719 | [0.831, 0.904] | 0.8036 | [0.753, 0.846] | [0.000, 0.012] |
| nvidia/nemotron-3-super-120b-a12b | 320 | 0.8531 | [0.810, 0.888] | 0.7321 | [0.677, 0.781] | [0.001, 0.018] |
| nvidia/nemotron-3-ultra-550b-a55b | 320 | 0.875 | [0.834, 0.907] | 0.8107 | [0.761, 0.852] | [0.000, 0.012] |
| openai/gpt-oss-120b | 171 | 0.9064 | [0.853, 0.942] | 0.7753 | [0.678, 0.850] | [-0.000, 0.022] |
| openai/gpt-oss-20b | 85 | 0.8706 | [0.783, 0.926] | 0.9167 | [0.646, 0.985] | [0.000, 0.043] |
| qwen/qwen3-32b | 320 | 0.8812 | [0.841, 0.912] | 0.7286 | [0.674, 0.777] | [0.000, 0.012] |
| qwen/qwen3.6-27b | 320 | 0.8875 | [0.848, 0.918] | 0.7357 | [0.681, 0.784] | [0.000, 0.012] |
| z-ai/glm-5.2 | 90 | 0.9 | [0.821, 0.947] | 0.7733 | [0.667, 0.853] | [0.000, 0.041] |

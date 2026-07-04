# ClinMAP-VOI v0 performance metrics

Run: `hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped`
Reviewer: **Tarek Etman**

- Mean decision accuracy: **0.891**
- Mean metamorphic pass rate: **0.786**

| model | rows | decision accuracy | metamorphic pass | clinical safety |
|---|---:|---:|---:|---:|
| gemma-4-31b | 320 | 0.859 | 0.750 | 3.497 |
| meta-llama/llama-4-scout-17b-16e-instruct | 320 | 0.903 | 0.814 | 3.591 |
| meta/llama-3.3-70b-instruct | 320 | 0.925 | 0.796 | 3.728 |
| mistral-large-2512 | 320 | 0.891 | 0.775 | 3.469 |
| mistral-medium-2508 | 320 | 0.894 | 0.814 | 3.487 |
| mistral-small-2603 | 320 | 0.872 | 0.804 | 3.528 |
| nvidia/nemotron-3-super-120b-a12b | 320 | 0.853 | 0.732 | 3.522 |
| nvidia/nemotron-3-ultra-550b-a55b | 320 | 0.875 | 0.811 | 3.634 |
| qwen/qwen3-32b | 320 | 0.881 | 0.729 | 3.763 |
| qwen/qwen3.6-27b | 320 | 0.887 | 0.736 | 3.775 |
| openai/gpt-oss-120b | 171 | 0.906 | 0.775 | 3.784 |
| gpt-oss-120b | 140 | 0.907 | 0.677 | 3.779 |
| deepseek-ai/deepseek-v4-pro | 137 | 0.934 | 0.798 | 3.431 |
| magistral-medium-2509 | 127 | 0.890 | 0.900 | 3.622 |
| z-ai/glm-5.2 | 90 | 0.900 | 0.773 | 3.333 |
| openai/gpt-oss-20b | 85 | 0.871 | 0.917 | 3.694 |
| gemini-3.5-flash | 21 | 0.905 | 0.765 | 3.714 |

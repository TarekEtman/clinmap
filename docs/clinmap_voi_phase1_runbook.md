# ClinMAP-VOI Phase 1 Runbook

## Build and validate

```bash
make clinmap-voi
```

This regenerates the synthetic decision-family dataset, validates the strict record contract, and writes design metrics.

## Dry-run a local Ollama collection

```bash
python3 model_runs/run_ollama_clinmap_voi.py \
  --model qwen2.5:7b-instruct \
  --limit 16 \
  --dry-run
```

## Run a pilot after Ollama is installed

```bash
python3 model_runs/run_ollama_clinmap_voi.py \
  --model qwen2.5:7b-instruct \
  --limit 16 \
  --temperature 0.2
```

Recommended pilot: 16 prompts first, then 40, then the full 320-prompt pack per model.

## Full local run pattern

Use one model at a time. Keep the machine awake and plugged in.

```bash
caffeinate -dimsu python3 model_runs/run_ollama_clinmap_voi.py \
  --model qwen2.5:14b-instruct \
  --temperature 0.2
```

Outputs are written to:

```text
model_runs/outputs/clinmap_voi_v0/
```

## Build a human-review queue

Blind review queue:

```bash
python3 clinmap_voi/build_review_queue_v0.py \
  model_runs/outputs/clinmap_voi_v0/<run_id>.jsonl
```

Unblind adjudication queue:

```bash
python3 clinmap_voi/build_review_queue_v0.py \
  model_runs/outputs/clinmap_voi_v0/<run_id>.jsonl \
  --unblind
```

## Publication gate

Do not publish model-level metrics until:

1. model run manifest exists;
2. failed rows are declared;
3. human review queue is complete;
4. relation annotations include evidence spans;
5. unresolved high-risk adjudications are resolved;
6. the report avoids clinical-validation or model-safety claims.

## Hosted API main benchmark path

The main run should use hosted APIs first because it gives stronger model coverage and faster throughput than local-only execution.

Set keys only in the shell environment:

```bash
export GROQ_API_KEY="..."
export CEREBRAS_API_KEY="..."
export MISTRAL_API_KEY="..."
```

Probe model availability:

```bash
python3 model_runs/run_hosted_clinmap_voi.py --probe-models
```

Run ladder:

```bash
# 1 prompt × selected models
python3 model_runs/run_hosted_clinmap_voi.py --limit 1 --max-workers 12

# 16 prompts × selected models
python3 model_runs/run_hosted_clinmap_voi.py --limit 16 --max-workers 12

# full 320 prompts × 12 configured hosted models
python3 model_runs/run_hosted_clinmap_voi.py --full --max-workers 12
```

If a provider rate-limits, rerun the same command with the same `--run-id`; completed rows are skipped unless `--retry-failed` is passed.

Summarize:

```bash
python3 clinmap_voi/summarize_hosted_run_v0.py \
  model_runs/outputs/hosted_clinmap_voi_v0/<run_id>.jsonl
```

Recommended provider order for smoke testing:

1. Groq `qwen/qwen3.6-27b`
2. Cerebras `gpt-oss-120b`
3. Mistral `mistral-large-2512`
4. all configured models

## Main-run provider decision

Use only the confirmed main providers for the first serious hosted corpus:

- Groq
- Cerebras
- Mistral

Do not include these in the main run yet:

- Google AI Studio — exact usable Gemini limits not captured.
- NVIDIA NIM — visible RPM exists, daily/token caps unclear.
- AnyAPI — daily token conversion unclear.
- OpenRouter — free models exist, request/day limits unclear.
- DeepSeek direct — free quota not confirmed.

Reason: the goal is a clean, reproducible first corpus, not maximum provider chaos. Additional providers can become a v1.1 expansion after the first 3,840-output corpus is collected and summarized.

## Safe-speed main run limits

All runs use:

```json
{
  "temperature": 0,
  "top_p": 1,
  "max_tokens": 180,
  "target_total_tokens_per_request": "<500"
}
```

Configured safe RPM per model:

| Provider | Model | Safe RPM |
|---|---|---:|
| Cerebras | `gpt-oss-120b` | 4 |
| Cerebras | `gemma-4-31b` | 4 |
| Cerebras | `zai-glm-4.7` | 4 |
| Groq | `meta-llama/llama-4-scout-17b-16e-instruct` | 20 |
| Groq | `qwen/qwen3-32b` | 8 |
| Groq | `qwen/qwen3.6-27b` | 8 |
| Groq | `openai/gpt-oss-120b` | 8 |
| Groq | `openai/gpt-oss-20b` | 8 |
| Mistral | `mistral-large-2512` | 3.5 |
| Mistral | `magistral-medium-2509` | 4 |
| Mistral | `mistral-medium-2508` | 18 |
| Mistral | `mistral-small-2603` | 30 |

The runner writes every completed row immediately, respects `Retry-After` / rate-limit headers when present, uses exponential backoff, and skips completed rows on resume.

## Supplementary provider probes: Google and NVIDIA

Google and NVIDIA are optional expansion providers. They do not replace the core Groq/Cerebras/Mistral run.

### Google AI Studio / Gemini OpenAI-compatible endpoint

Official OpenAI-compatible base URL:

```text
https://generativelanguage.googleapis.com/v1beta/openai/
```

Environment variable:

```bash
export GEMINI_API_KEY="..."
```

Probe Google first:

```bash
python3 model_runs/run_hosted_clinmap_voi.py \
  --providers google \
  --include-supplementary \
  --limit 20 \
  --max-workers 2
```

If the 20-prompt probe succeeds without unacceptable 429/errors, run full Google supplementary corpus:

```bash
python3 model_runs/run_hosted_clinmap_voi.py \
  --providers google \
  --include-supplementary \
  --full \
  --max-workers 2
```

Configured Google models:

- `gemini-3.1-pro`
- `gemini-3.5-flash`

### NVIDIA NIM / NVIDIA Build OpenAI-compatible endpoint

NVIDIA requires the exact OpenAI-compatible base URL and model IDs shown in the NVIDIA Build playground.

Set:

```bash
export NVIDIA_API_KEY="..."
export NVIDIA_BASE_URL="<NVIDIA Build OpenAI-compatible base URL>"
export NVIDIA_MODEL_1="<best visible Nemotron/chat model ID>"
export NVIDIA_MODEL_2="<best visible Llama/Qwen/Mistral chat model ID>"
```

Probe NVIDIA first:

```bash
python3 model_runs/run_hosted_clinmap_voi.py \
  --providers nvidia \
  --include-supplementary \
  --limit 20 \
  --max-workers 2
```

If successful, run full NVIDIA supplementary corpus:

```bash
python3 model_runs/run_hosted_clinmap_voi.py \
  --providers nvidia \
  --include-supplementary \
  --full \
  --max-workers 2
```

If both Google and NVIDIA are configured and pass probes, the expanded maximum corpus is:

```text
16 models × 320 prompts = 5,120 raw outputs
```

Supplementary-provider errors should not block the core 3,840-output benchmark.

### Current NVIDIA primary model

Configured NVIDIA primary supplementary model:

```text
nvidia/nemotron-3-ultra-550b-a55b
```

Current NVIDIA base URL:

```text
https://integrate.api.nvidia.com/v1
```

For benchmark consistency, the runner does **not** use the playground sample settings `temperature=1`, `max_tokens=16384`, streaming, or large reasoning budget. It uses the same benchmark settings as every other provider:

```json
{
  "temperature": 0,
  "top_p": 1,
  "max_tokens": 180
}
```

### Current NVIDIA expanded model set

Configured NVIDIA supplementary text models:

```text
nvidia/nemotron-3-ultra-550b-a55b
nvidia/nemotron-3-super-120b-a12b
z-ai/glm-5.2
deepseek-ai/deepseek-v4-pro
```

Reason for adding DeepSeek V4 Pro: it adds an independent DeepSeek MoE coding/reasoning family. Kimi K2.6 was not chosen for the main expansion because NVIDIA's page indicates deprecation on 2026-07-07, and another Mistral model would overlap with the core Mistral provider run.

Current maximum expanded corpus:

```text
18 models × 320 prompts = 5,760 raw outputs
```

### Current NVIDIA baseline model

Configured NVIDIA baseline model:

```text
meta/llama-3.3-70b-instruct
```

Reason: it is not a headline new frontier model, but it is a widely recognized Meta baseline that helps contextualize the newer Nemotron, GLM, and DeepSeek outputs.

Current maximum expanded corpus with this baseline:

```text
19 models × 320 prompts = 6,080 raw outputs
```

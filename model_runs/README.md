# Model Runs

This folder is reserved for real model-output runs.

Current status: `pending_credentials`.

No real model-provider outputs are included in the public v1 demo. When a run is added, each response must record provider, model ID, model snapshot/date, prompt hash, run ID, temperature, tool access, response origin, and redaction status.

## ClinMAP-VOI hosted benchmark runner

The primary benchmark path is hosted API collection across Groq, Cerebras, and Mistral. Local Ollama remains optional and is not required for the main run.

Required environment variables, depending on which providers are run:

```bash
export GROQ_API_KEY="..."
export CEREBRAS_API_KEY="..."
export MISTRAL_API_KEY="..."
```

No keys are stored in the repository.

Plan the full run:

```bash
python3 model_runs/run_hosted_clinmap_voi.py --plan --full
```

Probe provider model availability:

```bash
python3 model_runs/run_hosted_clinmap_voi.py --probe-models
```

One-prompt smoke test across all configured models:

```bash
python3 model_runs/run_hosted_clinmap_voi.py --limit 1 --max-workers 12
```

Sixteen-prompt pilot:

```bash
python3 model_runs/run_hosted_clinmap_voi.py --limit 16 --max-workers 12
```

Full 320-prompt × 12-model corpus:

```bash
python3 model_runs/run_hosted_clinmap_voi.py --full --max-workers 12
```

Summarize a run:

```bash
python3 clinmap_voi/summarize_hosted_run_v0.py \
  model_runs/outputs/hosted_clinmap_voi_v0/<run_id>.jsonl
```

Generated rows are raw model outputs only. They are not clinical validation, model ranking, or scored safety claims until a separate annotation/adjudication stage is complete.

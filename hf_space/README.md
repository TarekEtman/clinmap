# Hugging Face Space Scaffold - Clinical Model Behavior Eval Explorer

This optional Space wraps the **v1 synthetic demo** (supporting lineage). The repo’s primary deliverable is **ClinMAP-VOI v0** (see root `README.md`). It is not required for the repo to work, and it is not included in automated tests because `gradio` may not be installed locally.

## Intended use

- Browse cases and candidate responses.
- Filter by task type and risk level.
- Inspect scores, failure tags, and rationales.
- Demonstrate evaluation-system thinking to technical reviewers.

## Claim boundary

Synthetic demo only. Not medical advice, not a model benchmark, not clinical validation.

## Files to include when publishing a Space

- `hf_space/app.py`
- `data/v1/*.jsonl`
- `data/v1/dataset_manifest.json`

## Run locally

```bash
pip install gradio
python hf_space/app.py
```

# OpenAI-Evals-Style Adapter

This adapter exports the v1 synthetic cases into a portable JSONL format inspired by chat-eval workflows:

- `input`: user message(s)
- `ideal`: expected safe behavior anchors
- `disallowed`: unsafe behavior anchors
- `metadata`: case/task/risk/taxonomy fields
- `candidates`: included A/B fixture responses with expected scores for local regression checks

This is a portability starting point, not a claim that the file is a drop-in config for every version of any external eval package.

Generate:

```bash
python3 adapters/openai_evals/export_v1_openai_evals.py
```

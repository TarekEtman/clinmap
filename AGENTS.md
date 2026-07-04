# Agent instructions

**Canonical project root:** `/Users/nati/Documents/JOB/ClinMAP` (this repository).

**If the agent cannot run terminal commands:** reopen this folder in Grok/Cursor. See `docs/WORKSPACE_SETUP.md`.

**Primary deliverable:** ClinMAP-VOI v0 hosted benchmark — review complete. Start with `README.md` and `docs/deliverables_index.md`.

**Finalization index:** `report/hosted_runs/hosted_clinmap_voi_v0_finalization_20260704.md`

## Operating rules

- Do not publish, email, DM, or do external outreach without explicit user confirmation.
- Do not ask for API keys in chat; use zsh-safe local prompts in terminal scripts only.
- Keep provenance clean; do not relabel raw model rows.
- Public materials must follow `.public_boundary.md` if present.
- Do not reference or modify any legacy duplicate tree; work only in this repo.

## Key commands

```bash
make clinmap-frontier-pack   # evidence + holdout panel + QA audit
make clinmap-review-audit
make audit
python3 -m unittest discover -s tests
```

Holdout-panel publication QA uses frozen `data/clinmap_voi_v0/panel_holdout_reviews.jsonl`; recompute metrics with `make clinmap-holdout-panel`. Do not regenerate panel labels during routine audit.

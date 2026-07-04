# Agent instructions

**Canonical project root:** `/Users/nati/Documents/JOB/clinical-ai-eval-lab-v1` (this repository).

**If the agent cannot run terminal commands:** workspace path may be wrong (`clinical-ai-eval-lab` vs `-v1`). See `docs/WORKSPACE_SETUP.md` — symlink script `scripts/fix_workspace_symlink.sh` or reopen this folder in Grok/Cursor.

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
make clinmap-frontier-pack   # evidence + holdout dual AI + QA audit
make clinmap-review-audit
make audit
python3 -m unittest discover -s tests
```
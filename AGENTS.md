# Agent instructions

**Canonical project root:** `clinical-ai-eval-lab-v1` (this repository).

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
make clinmap-review-audit
make audit
python3 -m unittest discover -s tests
```
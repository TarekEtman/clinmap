# Limitations and non-clinical use — ClinMAP-VOI v0

## Limitations

- **Synthetic probes** — Cases are designed metamorphic families, not a sample of real patient encounters or live clinical workflows.
- **Not clinical validation** — No patient outcomes, prospective trials, or provider-performance claims.
- **Single named primary reviewer** on the full corpus (Tarek Etman); protocol QC passes supplement but do not replace an independent multi-human panel on all rows.
- **Holdout independent panel (Layer C)** — Pseudonymous external independent reviewers `panel_r01` / `panel_r02` on CMVOI-033–040; status in `data/clinmap_voi_v0/panel_holdout_status.json`. Optional additional holdout waves via `make clinmap-panel-pack`.
- **Hosted model coverage** — v0 leaderboard reflects models successfully collected in the canonical run (17 in metrics); partial runs and provider outages are documented in finalization notes.
- **English, text-only** — No multimodal, tool-use, or EHR integration in v0.

## What v0 *is* (scope correction)

- **3,971** reviewed response rows and **3,219** relation annotations on a **frozen** hosted run — not a small illustrative demo.
- **Multi-model** hosted comparison under one rubric — not a single-model case study.
- **Explicit claim boundaries** in evaluation card, QA audit, and benchmark evidence reports.

## Non-clinical use statement

This project is not intended for patient care, diagnosis, treatment, triage, or medical decision-making. It is an evaluation-systems artifact: structured rubrics, review protocols, metamorphic constraints, and reproducible reporting for **healthcare-domain model behavior**.

## Why synthetic examples are used

Synthetic metamorphic families demonstrate evaluation method without patient data, employer content, or proprietary clinical records. Construct validity is argued in `docs/construct_validity_clinmap_voi_v0.md`; external panel validation is described in `docs/panel_review_strategy.md`.

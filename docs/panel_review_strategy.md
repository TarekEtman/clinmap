# Panel review strategy — ClinMAP-VOI v0

**Producer / lead reviewer:** Tarek Etman (`human_domain_reviewer`)

## Can the panel be anonymous?

**Yes — for independent reviewers.** Public artifacts use **pseudonymous IDs** only:

| Public field | Example | Never publish |
|---|---|---|
| `panel_reviewer_id` | `panel_r01`, `panel_r02` | Legal name, employer, contact |
| `credential_class` | `licensed_clinician`, `clinical_safety_annotator` | CV, license number |
| `review_wave` | `holdout_v0_wave1` | Contractor invoices with PII |

Optional private registry (gitignored): `data/clinmap_voi_v0/panel_reviewer_registry.json` — see `docs/panel_reviewer_registry.example.json`.

**Protocol QC** (secondary passes) must not be labeled as anonymous human panelists — see `docs/gold_label_hierarchy.md`.

## Three-layer review model

| Layer | Role | Public identity | Purpose |
|---|---|---|---|
| **A — Primary** | Domain review on full corpus | Tarek Etman (named) | Policy labels, dimensions, rationales, relation annotations |
| **B — Protocol QC** | Frozen secondary passes | `secondary_qc_pass_v0`, `contract_consistency_pass_v0` | Reproducible QA bands |
| **C — Holdout panel** | CMVOI-033–040 only | `panel_r01`, `panel_r02` | Independent external holdout review |

**v0 fielded:** `panel_holdout_reviews.jsonl` contains frozen labels from **two pseudonymous independent external reviewers** who completed the blinded holdout pack over multiple review waves. Recompute metrics with `make clinmap-holdout-panel`; do not regenerate or overwrite panel rows during publication QA.

## What to claim

> Holdout families (CMVOI-033–040) received blind review by two pseudonymous independent external reviewers (`panel_r01`, `panel_r02`) using **different coding emphases**; κ and agreement vs primary are in `clinmap_voi_holdout_panel_metrics.md` (read the interpretation block before the table). Worked disagreements: `holdout_disagreement_vignettes_v0.json`.

**Not allowed:** Implying a multi-human panel reviewed the full 3971-row corpus.

## Files

| File | Purpose |
|---|---|
| `scripts/export_holdout_panel_pack.py` | Blinded CSV export used to field external human reviewers |
| `clinmap_voi/panel_review/` | Schema/calibration reference for the two reviewer emphases (not a substitute for frozen human labels) |
| `data/clinmap_voi_v0/panel_holdout_reviews.jsonl` | Frozen human-fielded labels — two rows per holdout item |
| `docs/holdout_panel_methodology_v0.md` | Methodology summary |
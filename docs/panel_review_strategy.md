# Panel review strategy — ClinMAP-VOI v0

**Producer / lead reviewer:** Tarek Etman (`human_domain_reviewer`)

## Can the panel be anonymous?

**Yes — for real independent reviewers.** Public artifacts should use **pseudonymous IDs** only:

| Public field | Example | Never publish |
|---|---|---|
| `panel_reviewer_id` | `panel_r01`, `panel_r02` | Legal name, employer, contact |
| `credential_class` | `licensed_clinician`, `clinical_safety_annotator` | CV, license number |
| `review_wave` | `holdout_v0_wave1` | Contractor invoices with PII |

Maintain an optional **private registry** (gitignored): `data/clinmap_voi_v0/panel_reviewer_registry.json` — maps pseudonym → real identity for your records and due diligence if a lab asks under NDA. See `docs/panel_reviewer_registry.example.json`.

**No — for synthetic or protocol automation.** Do **not** label blind QC / contract passes or rule-based engines as “anonymous panel reviewers.” That is misrepresentation. Those layers are **protocol QC passes** (documented in `docs/gold_label_hierarchy.md`).

## Three-layer review model (honest)

| Layer | Role | Public identity | Purpose |
|---|---|---|---|
| **A — Primary** | Domain review on full corpus | Tarek Etman (named) | Policy labels, dimensions, rationales, relation annotations |
| **B — Protocol QC** | Frozen secondary passes | `secondary_qc_pass_v0`, `contract_consistency_pass_v0` (code modules) | Reproducible QA bands; not a human panel |
| **C — Holdout review** | CMVOI-033–040 only | **Option 1:** human `panel_r*` (anon OK) · **Option 2:** dual **AI protocol** raters | Extra validity signal on holdout slice |

**v0 default (Option 2):** `make clinmap-holdout-ai` — two **different** AI methodologies on holdout, fully disclosed (`rater_type: ai_protocol`). See `report/benchmark_evidence/clinmap_voi_holdout_dual_ai_metrics.md`.

| AI rater ID | Methodology |
|---|---|
| `ai_protocol_contract_v0` | Contract-first: framework anchor + evidence-forced overrides |
| `ai_protocol_escalation_v0` | Escalation-behavioral: response feature bands; **no** row `expected_policy_label` anchor |

**Human holdout (Option 1)** still available via `make clinmap-panel-pack` — do not mix human IDs with AI rows without updating `panel_holdout_status.json`.

## When to field Layer C (recommended before broad frontier-lab push)

1. Export blind pack: `python3 scripts/export_holdout_panel_pack.py`
2. Two reviewers with `credential_class` documented (anon IDs in JSONL)
3. Blinded to **model_id**; may see variant text and response
4. Target: **≥80 stratified rows** on holdout families (or full holdout slice if feasible)
5. Merge into `data/clinmap_voi_v0/panel_holdout_reviews.jsonl`
6. Run `python3 clinmap_voi/benchmark_evidence_reports_v0.py` and update QA audit narrative

## What to claim after Layer C

**Dual AI (Option 2) — allowed:**

> Holdout families (CMVOI-033–040) were scored by two independent **AI annotation protocols** with different methodologies; κ and agreement vs primary review are in `clinmap_voi_holdout_dual_ai_metrics.md`.

**Human panel (Option 1) — allowed:**

> Holdout families received blind review by N anonymized **human** clinical annotators (panel_r*); disagreement and κ reported in benchmark evidence.

**Not allowed:**

> Calling AI protocol raters “anonymous expert clinicians” or implying a human panel reviewed the full 3971-row corpus.

## Recruiting anon panel (practical)

- Colleagues under verbal NDA → pseudonyms only in repo
- Contract annotators (clinical safety / RN / dentist) → pay per row, no names in git
- Do **not** invent panel members in JSONL

## Files

| File | Purpose |
|---|---|
| `scripts/export_holdout_panel_pack.py` | Blinded CSV for external human reviewers |
| `scripts/run_holdout_dual_ai_review_v0.py` | Dual AI protocol on holdout |
| `clinmap_voi/holdout_ai_rater_contract_v0.py` | AI rater A |
| `clinmap_voi/holdout_ai_rater_escalation_v0.py` | AI rater B |
| `clinmap_voi/panel_holdout_metrics_v0.py` | κ / agreement report |
| `data/clinmap_voi_v0/panel_holdout_reviews.jsonl` | One row per rater judgment (2 lines per holdout item for dual AI) |
| `data/clinmap_voi_v0/panel_holdout_status.json` | Fielding status and plan |
| `docs/panel_reviewer_registry.example.json` | Template for private registry |
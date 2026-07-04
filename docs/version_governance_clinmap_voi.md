# Version governance — ClinMAP-VOI

## v0 (frozen — this repository state)

- **40 families / 320 variants / 280 relations**
- Hosted run `hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped`
- Primary review complete (Tarek Etman)
- Benchmark evidence reports versioned with `generated_at` in JSON

**Immutable for comparability:** prompt hashes, framework gold on variants, published queue CSV, relation annotations for this run ID.

## Patch policy (v0.x documentation only)

Allowed without new run ID:

- Docs, evidence reports, charts, QA audit wording
- `panel_holdout_reviews.jsonl` **addition** (new layer; document in provenance)
- Bug fixes in **verification** scripts that do not alter stored labels

## Minor version (v0.1)

Requires changelog entry and new manifest when any of:

- New families or variants
- Changed relation oracle expectations
- Re-review of existing rows with new primary labels
- New hosted run ID promoted to canonical

## Major version (v1)

Breaking schema changes, different policy label taxonomy, or incompatible metric definitions.

## Holdout families

CMVOI-033 through CMVOI-040 — reserved at design for QA and independent panel. Do not use for rubric calibration anecdotes in public claims without noting holdout status.
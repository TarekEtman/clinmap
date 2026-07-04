# Frontier Readiness Audit

Status: **ClinMAP-VOI v0 benchmark + frontier evidence bundle complete (local)**  
Date: 2026-07-04

## What is strong (frontier-lab reviewer path)

- **Frozen hosted benchmark:** 3971 reviewed rows, 3219 relation annotations, 17 models, canonical run ID `…deduped`.
- **Named primary domain review:** Tarek Etman (`human_domain_reviewer`); provenance in `benchmark_provenance.json` and `PRODUCER.md`.
- **Protocol QC on full corpus:** `secondary_review_pass.jsonl` (blind QA + contract passes) with κ in published band.
- **Holdout Layer C:** Independent external panel `panel_r01` / `panel_r02`, 720 items fielded, metrics in `clinmap_voi_holdout_panel_metrics.md`.
- **Construct validity + stats pack:** Wilson CIs, gold independence, accuracy vs metamorphic discrimination, failure atlas, adjudication summary (`make clinmap-frontier-pack`).
- **QA audit gates:** `overall_pass` including relation integrity recomputed from published queue + response features.
- **Governance docs:** replication guide, version freeze, gold hierarchy, holdout panel methodology, limitations.
- **Supporting v1 demo:** 48-case synthetic lineage without competing with headline benchmark.

## What remains weaker than production clinical eval (state honestly)

- Not a multi-human panel on the **full** queue — protocol QC + pseudonymous holdout-panel slice only.
- Synthetic text probes — no EHR, multimodal, or outcome-linked validation.
- Some hosted aliases have partial/rate-limited collection (documented; not required to claim v0 freeze).
- Holdout κ between the two pseudonymous independent external reviewers is moderate (~0.50) — expected for different coding emphases; report alongside κ vs primary.

## What not to claim

- Clinical validation, production safety certification, or unconstrained healthcare performance ranking.
- Multi-human panel on the full queue (protocol QC + holdout slice only in v0).
- 100% agreement between framework gold and primary labels (by design; stats are reported).

## Refresh before outreach

```bash
make clinmap-frontier-pack
make clinmap-pdf
make audit
```

Entry points: `README.md`, `docs/deliverables_index.md`, `docs/frontier_lab_evidence_checklist.md`, `docs/privacy_and_claims_clinmap_voi_v0.md`.

## Stop line

Portfolio / eval-systems evidence only. Peer-reviewed clinical evidence and deployment sign-off are out of scope for v0.
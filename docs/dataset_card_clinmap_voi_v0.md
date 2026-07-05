# Dataset Card — ClinMAP-VOI v0

## Dataset summary

Synthetic healthcare **decision-family** benchmark: metamorphic prompt variants, hosted LLM responses, human domain review labels, and pairwise relation annotations.

**Benchmark producer and primary reviewer:** Tarek Etman (`human_domain_reviewer`) — see [`benchmark_provenance.json`](../data/clinmap_voi_v0/benchmark_provenance.json) and [`PRODUCER.md`](PRODUCER.md).

## Dataset type

Synthetic evaluation corpus for **clinical-AI policy behavior** (escalation, VOI, medication boundary, pressure resistance)—not a clinical outcomes dataset.

## Languages

English.

## Structure

| File | Description |
|---|---|
| `decision_families.jsonl` | 40 families with decisive variables, VOI slots, leakage groups |
| `variants.jsonl` | 320 variants (8 per family), one primary changed fact per variant |
| `metamorphic_relations.jsonl` | 280 expected cross-variant behavior relations |
| `model_prompt_pack.jsonl` | Prompts used for hosted runs |
| `source_context.jsonl` | Synthetic context anchors (no PHI) |
| `relation_annotations.jsonl` | Reviewer metamorphic pass/fail per model × relation |
| `adjudications.jsonl` | High-risk / low-confidence adjudication records |

## Hosted outputs

Collected via `model_runs/run_hosted_clinmap_voi.py` into `model_runs/outputs/hosted_clinmap_voi_v0/`. Canonical deduped run for this release:

`hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped`

Review corpus and queue are derived from that run (see README).

## Reviewed subset

- **3971** rows with non-empty model responses reviewed.
- **17** models represented in aggregate metrics.
- Holdout evaluation on families **CMVOI-033** through **CMVOI-040** (see QA audit).

## Excluded data

No patient data, PHI, employer/platform tasks, client rubrics, or confidential model deployments.

## Splits

Family-level holdout defined in framework manifest and audit (families 033–040 held out for QA reporting).

## Citation / provenance

Producer: Tarek Etman. Framework version: `clinmap-voi-v0.1` (see `data/clinmap_voi_v0/manifest.json`).

## Related cards

- Synthetic v1 demo (smaller separated object model): `docs/dataset_card_v1.md`
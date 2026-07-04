# ClinMAP-VOI Phase 1 Design Metrics

Status: design metrics only. No model-output performance or ranking is claimed.

## Counts

| Item | Count |
|---|---:|
| decision families | 40 |
| variants | 320 |
| metamorphic relations | 280 |
| model prompts | 320 |
| source context records | 4 |
| metric blueprint records | 10 |

## Relation-oracle coverage

| Metric | Value |
|---|---:|
| complete families | 40 |
| complete family rate pct | 100.0 |
| one primary changed fact variants | 320 |
| one primary changed fact rate pct | 100.0 |
| action change variants | 240 |
| invariant variants | 80 |
| action change relations | 200 |
| invariant relations | 80 |

## Variant types

| Variant type | Count |
|---|---:|
| contraindication_or_medication_risk | 40 |
| followup_correction | 40 |
| high_risk_context_shift | 40 |
| low_risk_control | 40 |
| missing_context | 40 |
| nuisance_invariance | 40 |
| urgent_red_flag | 40 |
| user_pressure | 40 |

## Relation types

| Relation type | Count |
|---|---:|
| contraindication_sensitivity | 40 |
| directional_safety_monotonicity | 40 |
| nuisance_invariance | 40 |
| pressure_resistance | 40 |
| safety_hysteresis_update | 40 |
| urgent_red_flag_dominance | 40 |
| voi_request_increase | 40 |

## Claim boundary

This Phase 1 package is a synthetic, relation-labeled evaluation method and local-run-ready prompt pack. It is not a clinical validation, not a healthcare benchmark, not patient advice, and not a model ranking.

## Next gates

- run local model pilot on a 16-40 prompt subset
- collect actual model outputs with run manifests
- create blinded human review queue
- score relation annotations with evidence spans
- compute model-level metrics only after review completion

# Construct validity — ClinMAP-VOI v0

## What ClinMAP measures

**Policy behavior under clinically meaningful perturbations**, not document QA or diagnosis accuracy.

Core construct: *When decisive facts change (or VOI is missing), does the model’s implied action policy move in the direction the rubric demands?*

## Relation types → deployment failure modes

| Relation type | Failure mode in production health AI |
|---|---|
| `voi_request_increase` | Answers before asking action-changing questions |
| `directional_safety_monotonicity` | Fails to tighten when risk markers appear |
| `urgent_red_flag_dominance` | Reassurance or delay under red-flag language |
| `contraindication_sensitivity` | Treatment approval despite medication/context risk |
| `nuisance_invariance` | Over- or under-reacts to irrelevant surface details |
| `pressure_resistance` | Sycophancy — lowers threshold when user pressures |
| `safety_hysteresis_update` | Anchoring on prior benign framing after new facts |

## Why this is not redundant with decision accuracy

Single-turn accuracy scores each response against variant gold. **Metamorphic pass rate** scores **ordered pairs** across variants for the same model and family.

Evidence: `report/benchmark_evidence/clinmap_voi_v0_benchmark_discrimination.md` — model spread, variant-type difficulty, per-model risk gap (high-risk vs low-risk gold match).

Expect **ρ < 1** between accuracy and metamorphic pass across models; large spreads indicate the second metric carries separate information.

## Synthetic scope (explicit)

Probes are **designed** metamorphic families, not sampled from clinical practice. Validity claim:

> ClinMAP tests whether models satisfy stated policy constraints under controlled perturbations — a necessary (not sufficient) condition for safe health-domain assistants.

Bridge to public work: HealthBench (multi-axis rubrics), MedHELM (holistic medical eval), HealthAgentBench (agentic care) — ClinMAP contributes **pairwise metamorphic structure + VOI** (see `eval_spec/clinmap_voi_eval_spec_v0.md`).

## External validity path

1. **Now:** Discrimination + failure atlas + Wilson CIs on frozen v0
2. **Holdout (v0):** Two pseudonymous external independent reviewers on CMVOI-033–040 (`panel_r01`, `panel_r02`) — fielded blind holdout, different coding emphases, κ vs primary
3. **Optional upgrade:** Additional holdout waves via `make clinmap-panel-pack` with new `panel_r*` IDs
4. **Later (v0.1+):** Small real-world prompt audit — compare violation taxonomy overlap, not score transfer
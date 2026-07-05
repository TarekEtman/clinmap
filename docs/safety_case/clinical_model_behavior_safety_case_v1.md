# Safety Case - Clinical Model Behavior Evaluation v1

## Claim

The v1 proof system demonstrates that Tarek Etman can design and operate a structured healthcare-domain model behavior evaluation workflow while preserving privacy and claim boundaries.

## Evidence

| Evidence | File |
|---|---|
| Synthetic case design | `data/v1/cases.jsonl` |
| Explicit response provenance | `data/v1/responses.jsonl` |
| Rubric-based annotations | `data/v1/annotations.jsonl` |
| Disagreement handling | `data/v1/adjudications.jsonl` |
| Pairwise preference records | `data/v1/pairwise_preferences.jsonl` |
| Validation and metrics | `eval_harness/v1_validate.py`, `eval_harness/v1_metrics.py` |
| Evaluation card | `docs/evaluation_card_v1.md` |
| Privacy and claims audit | `docs/privacy_and_claims_audit.md` |

## Assumptions

- Synthetic cases are sufficient to demonstrate evaluation-system design.
- Public source anchors support evaluation methodology framing, not clinical claims.
- Two-pass self-calibration is useful for showing scoring discipline but does not replace independent reviewer reliability.

## Residual risks

- Synthetic-only evidence may be less persuasive than actual model-output runs.
- The dataset is small and selective.
- The current public artifacts do not prove production performance under live model conditions.

## Risk controls

- All public artifacts label synthetic data clearly.
- Automated tests block target-company mentions and meta-template candidate responses.
- The manifest excludes patient data, platform tasks, client materials, and proprietary rubrics.
- Actual model runs are isolated under `model_runs/` and require explicit credentials and permission.

## Decision

The v1 system is suitable as a public proof artifact for evaluation design, rubric calibration, and healthcare-domain model behavior review. It is not suitable for clinical deployment or benchmark claims.

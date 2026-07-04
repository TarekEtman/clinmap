# Governance Review Checklist

Use this checklist before publishing or sharing a new artifact.

## Public neutrality

- [ ] No target-company names.
- [ ] No internal role names or private hiring language.
- [ ] No exaggerated marketing claims.
- [ ] No claims of clinical deployment readiness.

## Privacy and confidentiality

- [ ] No patient data.
- [ ] No copied clinical notes.
- [ ] No platform task content.
- [ ] No proprietary prompts or rubrics.
- [ ] No screenshots containing private information.

## Clinical scope

- [ ] Clearly says the artifact is not medical advice.
- [ ] No diagnosis or treatment instruction presented as guidance.
- [ ] Medication content is framed as evaluation of model behavior, not advice.
- [ ] Human/professional review boundaries are clear.

## Evidence quality

- [ ] Synthetic cases are specific enough to test real failure modes.
- [ ] Rubric anchors are explicit.
- [ ] Failure labels map to taxonomy.
- [ ] Scripts run without private API keys.
- [ ] Limitations are stated.

## Anti-generic review

- [ ] Includes concrete scored examples.
- [ ] Includes at least one subtle fluent-but-unsafe failure.
- [ ] Includes at least one over-refusal or low-acuity calibration control.
- [ ] Includes reasoning/rationale audit, not only surface safety.
- [ ] Avoids broad claims unsupported by artifacts.

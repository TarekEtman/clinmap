# Designing Human-Evaluable Safety Probes for Healthcare-Domain Model Behavior

## Abstract

Healthcare-domain model evaluation is difficult because many failures are not obvious factual errors. A response can be fluent, empathetic, and apparently reasonable while still being unsafe: it may reassure too early, omit escalation, approve medication without context, or cite a rationale that does not follow from the prompt. This project presents a compact synthetic evaluation system that converts those ambiguous behaviors into inspectable human-data artifacts: cases, candidate responses, annotations, adjudications, pairwise preferences, metrics, charts, and release boundaries.

## Problem

Generic answer-quality review often overweights fluency and underweights risk-changing context. In healthcare-domain prompts, the decisive issue may be a missing constraint rather than a wrong statement. Evaluation systems therefore need rubrics that make uncertainty, escalation, scope, medication context, and reasoning faithfulness explicit.

## Method

The v1 demo uses 48 synthetic cases across 12 task types. Each case contains:

- prompt text;
- risk level;
- expected safe behavior;
- unsafe behavior;
- target failure modes;
- cap rules;
- source anchors for evaluation methodology;
- synthetic provenance metadata.

Each case includes two candidate responses. Responses are separated from annotations and explicitly labeled by origin. Annotations use eight dimensions: clinical safety, escalation, context sensitivity, factuality, uncertainty, scope control, usefulness, and rationale quality. Hard caps limit the maximum score when a response contains a high-impact safety failure.

## Results

The repository’s **headline artifact** is ClinMAP-VOI v0 (hosted benchmark, review complete; see README). The **synthetic v1 demo** contains 48 cases, 96 responses, 192 annotation records, 2 adjudications, and 48 pairwise preferences. A/B preferred positions are balanced 24/24. Two-pass self-calibration shows 83/96 exact score agreement and 96/96 within-one agreement. These are not independent reviewer reliability metrics.

## Key design decisions

### Separate objects

Cases, responses, annotations, adjudications, and preferences are separate files. This prevents a common portfolio problem: prose claims that cannot be inspected or rerun.

### Label provenance

Synthetic fixtures are not represented as real model outputs. Future actual model runs must use `actual_model_output` and retain provider/model/run metadata.

### Treat hard safety failures as caps

A response that gives unsafe delay advice or medication approval cannot receive a high score merely because it is fluent or otherwise helpful.

### Include over-refusal controls

A safe evaluation system should not reward blanket refusal on low-risk general-information prompts. Usefulness and calibration matter.

## Limitations

This is a synthetic demonstration, not a clinical benchmark. It does not validate real-world model safety, does not compare model providers, and does not claim additional reviewer reliability. The value is the evaluation architecture and reviewer judgment pattern.

## Future work

- Add real model-output runs with explicit provenance.
- Add independent reviewer passes for true inter-rater reliability.
- Expand holdout coverage by risk stratum and task type.
- Add an interactive explorer for non-technical reviewers.
- Package the dataset for reuse in external evaluation frameworks.

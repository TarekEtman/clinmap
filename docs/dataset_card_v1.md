# Dataset Card - Clinical Model Behavior v1 Synthetic Demo

> **Primary dataset card:** [`dataset_card_clinmap_voi_v0.md`](dataset_card_clinmap_voi_v0.md) (ClinMAP-VOI v0 hosted benchmark).

## Dataset summary

A synthetic healthcare-domain model behavior evaluation dataset with 48 cases, 96 candidate responses, 192 annotation records, 2 adjudications, and 48 pairwise preference records.

## Dataset type

Synthetic public demonstration dataset for evaluation-system design and reviewer calibration.

## Languages

English.

## Domains

Healthcare-domain model behavior review, including general triage wording, dental/oral-health context, medication-context safety, pregnancy context, pediatric context, public-health misinformation, clinical summarization, reasoning faithfulness, boundary management, and over-refusal controls.

## Provenance

All cases and responses are synthetic. Response records are explicitly labeled as:

- `synthetic_model_pattern`
- `expert_ideal`
- `human_baseline`
- `actual_model_output` if future runs are added

The current v1 public demo does not include actual model-provider outputs.

## Excluded data

No patient data, PHI, employer tasks, platform tasks, client materials, proprietary rubrics, or confidential model outputs.

## Splits

The dataset includes `dev` and `holdout` split fields for demonstration. The split is not intended for benchmark claims.

## Uses

Appropriate:

- inspecting evaluation-system architecture;
- testing schema/metrics pipelines;
- demonstrating rubric calibration;
- developing reviewer training examples;
- prototyping model-output scoring workflows.

Not appropriate:

- clinical decision-making;
- production model safety certification;
- model-provider leaderboard claims;
- medical advice generation;
- independent reliability claims.

## Biases and limitations

The dataset is intentionally small and synthetic. It reflects selected failure modes rather than full clinical coverage. It is designed to demonstrate judgment structure and data provenance, not real-world performance.

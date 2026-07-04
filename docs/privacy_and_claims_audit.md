# Privacy and Claims Audit - v1 Public Proof System

Status: **passes local release gate for synthetic public proof artifacts**  
Date: 2026-07-03

## Scope reviewed

- `eval_spec/clinical_model_behavior_eval_spec_v1.md`
- `data/v1/`
- `eval_harness/v1_*.py`
- `report/v1_synthetic_demo_report.md`
- `report/v1_charts/`
- `report/evaluation_systems_snapshot_v1.pdf`
- `public/explorer/`
- `exports/openai_evals/`
- `schemas/`
- `model_runs/`
- `hf_space/`
- `README.md`
- `docs/recruiter_snapshot.md`

## Privacy boundary

The v1 demo is synthetic-only. It does not use:

- patient data or PHI;
- employer/client/platform tasks;
- proprietary rubrics;
- confidential model outputs;
- internal hiring or routing information from any target company.

The dataset manifest explicitly declares `synthetic_only: true` and lists prohibited sources including `platform_tasks`, `client_materials`, and `proprietary_rubrics`.

## Claim boundary

Allowed claims:

- Tarek can design healthcare-domain synthetic evaluation probes.
- The repo demonstrates separated case/response/annotation/adjudication data architecture.
- The v1 harness validates schema integrity and computes demo metrics.
- Two-pass metrics are self-calibration metrics.

Disallowed claims:

- independent inter-rater reliability;
- clinical validation;
- production safety certification;
- real-world model benchmark results;
- evidence from private client or employer tasks.

## Current automated checks

`make audit` passes and includes:

- unit tests;
- target-company neutrality scan;
- v1 validation;
- v1 metrics;
- v1 chart generation;
- legacy MVP traceability checks.

## Residual risks

- The public proof system is synthetic, so it demonstrates evaluation design and judgment structure rather than real model access.
- The PDF is a reviewer snapshot, not a replacement for the full spec/data.
- If published, repository links should point to GitHub-hosted Markdown files or a static site build that preserves paths.

## Release decision

Approved for local portfolio packaging. External publishing or outreach still requires Tarek's explicit approval.

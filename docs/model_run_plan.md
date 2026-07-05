# Real Model Run Plan

## Purpose

The v1 repo currently uses synthetic fixtures. A real model run would add external model outputs while preserving the same case, response, annotation, and claim-boundary architecture.

## Run states

| State | Meaning |
|---|---|
| `pending_credentials` | Runner exists, but no API key or model access has been provided |
| `collected_unscored` | Model outputs collected but not annotated |
| `scored_local` | Outputs scored locally under the v1 rubric |
| `release_candidate` | Privacy/claim audit completed and artifacts ready for public review |

## Minimum acceptable real run

- Use 12-24 selected synthetic holdout prompts.
- Record provider, model ID, snapshot/date, temperature, system prompt, and tool access.
- Store raw model outputs separately from annotations.
- Do not mix real outputs with synthetic fixtures without explicit `response_origin` labels.
- Report metrics as a sample run, not a benchmark.

## Models

No real model outputs are currently included. This is intentional until credentials and publication permission are available.

## Claim boundary

A real run would support statements like: "I can operate an eval pipeline against actual model outputs." It would not support clinical performance claims, model safety certification, or broad provider rankings.

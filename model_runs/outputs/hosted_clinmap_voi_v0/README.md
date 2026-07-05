# Hosted ClinMAP-VOI v0 output provenance

This directory contains raw and derived hosted-run artifacts for ClinMAP-VOI v0.

## Canonical current project folder

Current working project folder:

```text
/Users/nati/Documents/JOB/ClinMAP
```

## Absolute paths in run manifests

Some `*_manifest.json` files preserve the absolute filesystem paths that existed at collection time, including paths under:

```text
/Users/nati/Documents/JOB/clinical-ai-eval-lab
```

Those paths are **immutable execution provenance**, not the current repository identity. They should not be rewritten in-place because the manifests document how the original hosted runs were executed. Public-facing docs and reproducibility instructions should use the canonical `ClinMAP` path above.

## Benchmark inclusion rule

The reviewed benchmark corpus is the main deduped/review corpus documented in:

- `report/hosted_runs/hosted_clinmap_voi_v0_finalization_20260704.md`
- `report/clinmap_voi_v0_performance_metrics.md`
- `report/clinmap_voi_review_quality_audit.md`

Supplementary Z.AI, Cloudflare, xAI, and direct-DeepSeek exploratory attempts are retained only as execution/provenance artifacts unless a future clean collection + review pass explicitly includes them under new aliases.

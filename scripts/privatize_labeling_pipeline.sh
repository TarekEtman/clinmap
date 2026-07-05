#!/usr/bin/env bash
# Move hosted review runner out of public tree; export frozen secondary-review pass.
# Public review protocol modules (stay in clinmap_voi/):
#   review_protocol_engine_v0.py primary_review_policy_v0.py
#   secondary_qc_pass_v0.py contract_consistency_pass_v0.py
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PRIV="$ROOT/.review_private/labeling_pipeline"
mkdir -p "$PRIV"
for f in run_hosted_review_pipeline_v0.py; do
  if [[ -f "$ROOT/clinmap_voi/$f" ]]; then
    mv "$ROOT/clinmap_voi/$f" "$PRIV/"
    echo "moved clinmap_voi/$f -> .review_private/labeling_pipeline/"
  fi
done
python3 "$ROOT/scripts/export_secondary_review_pass.py"
echo "Done. Commit data/clinmap_voi_v0/secondary_review_pass.jsonl and public clinmap_voi review protocol modules."
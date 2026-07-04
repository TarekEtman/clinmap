#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

usage() {
  cat <<'EOF'
Usage: scripts/stage_clinmap_v0_commit.sh [--check|--stage]

--check   Run release hygiene checks and show status without staging (default).
--stage   Run the same checks, then stage the intended public ClinMAP repo state.

This script never commits, pushes, deploys, posts, or sends outreach.
EOF
}

MODE="check"
case "${1:---check}" in
  --check) MODE="check" ;;
  --stage) MODE="stage" ;;
  -h|--help) usage; exit 0 ;;
  *) usage >&2; exit 2 ;;
esac

fail() { echo "ERROR: $*" >&2; exit 1; }

[ -f "README.md" ] || fail "run from ClinMAP repo root"
[ -f "ClinMAP.code-workspace" ] || fail "ClinMAP.code-workspace missing"
[ ! -f "clinical-ai-eval-lab-v1.code-workspace" ] || fail "stale clinical-ai-eval-lab-v1.code-workspace still exists"

# Secrets / private files must not be tracked or staged.
blocked_paths='(^|/)(\.env|\.env\..*|panel_reviewer_registry\.json|C_Tarek_Etman_V\.pdf)$|(^|/)\.review_private/|(^|/)node_modules/|(^|/)model_runs/logs/|(^|/)model_runs/tmp/|(^|/)tmp/'
if git ls-files | grep -E "$blocked_paths" >/dev/null; then
  git ls-files | grep -E "$blocked_paths" >&2
  fail "blocked private/generated paths are tracked"
fi

# Ban stale / misleading holdout and legacy identity wording.
if grep -RIn --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=dist \
  --exclude='*.jsonl' --exclude='*.csv' --exclude='*.png' --exclude='*.pdf' \
  --exclude='stage_clinmap_v0_commit.sh' \
  -E 'clinmap_voi_simulation|clinmap-holdout-ai|dual AI|Dual AI|AI protocol|AI rater|clinical-ai-eval-lab|frozen_pseudonymous_holdout_review_layer|holdout review layer' \
  README.md START_HERE.md docs clinmap_voi scripts src package.json package-lock.json 2>/dev/null; then
  fail "stale or downgraded holdout wording found"
fi

# Expected headline artifacts.
[ -f "report/clinmap_voi_v0_snapshot.pdf" ] || fail "ClinMAP snapshot PDF missing"
[ -f "public/assets/clinmap_voi_v0_snapshot.pdf" ] || fail "public ClinMAP snapshot PDF missing"
[ -f "report/hosted_runs/supplementary_provider_disposition_20260704.md" ] || fail "supplementary provider disposition missing"
[ -f "report/benchmark_evidence/clinmap_voi_holdout_panel_metrics.md" ] || fail "holdout panel metrics missing"

python3 - <<'PY'
import json
from pathlib import Path
status = json.loads(Path('data/clinmap_voi_v0/panel_holdout_status.json').read_text(encoding='utf-8'))
if status.get('layer_c_status') != 'fielded_external_holdout_panel':
    raise SystemExit(f"unexpected panel status: {status.get('layer_c_status')!r}")
prov = json.loads(Path('data/clinmap_voi_v0/benchmark_provenance.json').read_text(encoding='utf-8'))
holdout = prov.get('review_layers', {}).get('holdout_review', {})
if holdout.get('default_mode') != 'fielded_external_holdout_panel':
    raise SystemExit(f"unexpected provenance holdout mode: {holdout.get('default_mode')!r}")
if 'clinical-ai-eval-lab' in json.dumps(prov):
    raise SystemExit('stale workspace name in benchmark provenance')
PY

if [ "$MODE" = "check" ]; then
  echo "CHECK PASS: release hygiene looks clean. No files staged."
  git status -sb
  exit 0
fi

git add -A .

if git diff --cached --name-only | grep -E "$blocked_paths" >/dev/null; then
  git diff --cached --name-only | grep -E "$blocked_paths" >&2
  fail "blocked private/generated paths would be staged"
fi

echo "STAGE PASS: intended public repo state staged. Review carefully before commit."
git status -sb
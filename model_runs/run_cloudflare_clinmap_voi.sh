#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

CONFIG="model_runs/hosted_models_clinmap_voi_v0_free_candidates.json"
MODE="${1:-probe20}"          # probe20 | probe_models | full
MODELS="${CF_MODELS:-cloudflare_glm_4_7_flash_free_alloc}"
SHARDS="${CF_SHARDS:-3}"
WORKERS="${CF_WORKERS:-1}"
RETRIES="${CF_RETRIES:-3}"
TIMEOUT="${CF_TIMEOUT_SEC:-120}"
RPM_PER_SHARD="${CF_RPM_PER_SHARD:-10}"

ensure_cloudflare_env() {
  if [[ ! -t 0 && ( -z "${CLOUDFLARE_API_TOKEN:-}" || ( -z "${CLOUDFLARE_BASE_URL:-}" && -z "${CLOUDFLARE_ACCOUNT_ID:-}" ) ) ]]; then
    echo "Set CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID (or CLOUDFLARE_BASE_URL), or run this script interactively in Terminal." >&2
    exit 1
  fi

  # Token first — matches Cloudflare dashboard copy flow.
  if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
    printf "Enter CLOUDFLARE_API_TOKEN: " >&2
    IFS= read -r -s CLOUDFLARE_API_TOKEN
    printf "\n" >&2
    export CLOUDFLARE_API_TOKEN
  fi

  if [[ -z "${CLOUDFLARE_BASE_URL:-}" ]]; then
    if [[ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]]; then
      printf "Enter CLOUDFLARE_ACCOUNT_ID: " >&2
      IFS= read -r CLOUDFLARE_ACCOUNT_ID
      export CLOUDFLARE_ACCOUNT_ID
    fi
    export CLOUDFLARE_BASE_URL="https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/ai/v1"
  fi

  if [[ -z "${CLOUDFLARE_API_TOKEN:-}" || -z "${CLOUDFLARE_BASE_URL:-}" ]]; then
    echo "Cloudflare credentials were empty; aborting." >&2
    exit 1
  fi

  trap 'unset CLOUDFLARE_API_TOKEN CLOUDFLARE_ACCOUNT_ID' EXIT
}

write_temp_config() {
  local run_base="$1"
  local tmp_dir="model_runs/tmp/${run_base}"
  mkdir -p "$tmp_dir"
  python3 - <<PY
import json
from pathlib import Path

config_path = Path("${CONFIG}")
out_path = Path("${tmp_dir}/cloudflare_rpm${RPM_PER_SHARD}_config.json")
models = [m.strip() for m in "${MODELS}".split(",") if m.strip()]
rpm = int("${RPM_PER_SHARD}")

cfg = json.loads(config_path.read_text(encoding="utf-8"))
for model in cfg.get("models", []):
    if model.get("provider") == "cloudflare_workers_ai":
        model["enabled"] = model.get("alias") in models
        if model.get("alias") in models:
            model["rpm"] = rpm

out_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
print(out_path)
PY
}

launch_shards() {
  local run_base="$1"
  local cfg_path="$2"
  local log_dir="model_runs/logs/${run_base}"
  mkdir -p "$log_dir"

  echo "RUN_BASE=${run_base}"
  echo "LOG_DIR=${log_dir}"
  echo "MODELS=[${MODELS}] SHARDS=${SHARDS} RPM_PER_SHARD=${RPM_PER_SHARD}"

  : > "${log_dir}/${run_base}_pids.txt"
  pids=()
  for ((i=0; i<SHARDS; i++)); do
    python3 model_runs/run_hosted_clinmap_voi.py \
      --config "$cfg_path" \
      --run-id "${run_base}_shard${i}of${SHARDS}" \
      --models "$MODELS" \
      --include-supplementary \
      --full \
      --shard-index "$i" \
      --shard-count "$SHARDS" \
      --max-workers "$WORKERS" \
      --timeout-sec "$TIMEOUT" \
      --retries "$RETRIES" \
      > "${log_dir}/${run_base}_shard${i}of${SHARDS}.log" 2>&1 &
    pids+=("$!")
    last_pid="${pids[${#pids[@]} - 1]}"
    echo "${last_pid} ${run_base}_shard${i}of${SHARDS}" >> "${log_dir}/${run_base}_pids.txt"
  done

  echo "PIDS=${pids[*]}"
  echo "Monitor: tail -f ${log_dir}/${run_base}_shard*.log"
}

if [[ ! -f "$CONFIG" ]]; then
  echo "Missing config: $CONFIG" >&2
  exit 1
fi

ensure_cloudflare_env

case "$MODE" in
  probe_models)
    python3 model_runs/run_hosted_clinmap_voi.py \
      --config "$CONFIG" \
      --providers cloudflare_workers_ai \
      --include-supplementary \
      --probe-models \
      --timeout-sec "$TIMEOUT"
    ;;

  probe20)
    RUN_ID="hosted_clinmap_voi_v0_cloudflare_probe20_$(date -u +%Y%m%dT%H%M%SZ)"
    echo "RUN_ID=$RUN_ID"
    python3 model_runs/run_hosted_clinmap_voi.py \
      --config "$CONFIG" \
      --run-id "$RUN_ID" \
      --providers cloudflare_workers_ai \
      --include-supplementary \
      --limit 20 \
      --max-workers 3 \
      --timeout-sec "$TIMEOUT" \
      --retries "$RETRIES"
    ;;

  full)
    RUN_BASE="hosted_clinmap_voi_v0_cloudflare_smooth$((RPM_PER_SHARD * SHARDS))_$(date -u +%Y%m%dT%H%M%SZ)"
    CFG_PATH="$(write_temp_config "$RUN_BASE")"
    launch_shards "$RUN_BASE" "$CFG_PATH"
    ;;

  *)
    echo "Usage: $0 [probe20|probe_models|full]" >&2
    echo "Optional env: CF_MODELS, CF_SHARDS, CF_WORKERS, CF_RETRIES, CF_TIMEOUT_SEC, CF_RPM_PER_SHARD" >&2
    exit 2
    ;;
esac
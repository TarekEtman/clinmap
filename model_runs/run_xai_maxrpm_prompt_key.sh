#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

CONFIG="model_runs/hosted_models_clinmap_voi_v0_xai_maxrpm.json"
MODE="${1:-firehose}"      # firehose | firehose80 | firehose160 | full | turbo | probe80 | probe160 | probe20 | probe_models
SHARDS="${XAI_SHARDS:-8}"  # override: XAI_SHARDS=16 ./model_runs/run_xai_maxrpm_prompt_key.sh
MODELS="${XAI_MODELS:-xai_grok_4_3,xai_grok_build_0_1}"
WORKERS="${XAI_WORKERS:-2}"
RETRIES="${XAI_RETRIES:-4}"
TIMEOUT="${XAI_TIMEOUT_SEC:-120}"

if [[ ! -f "$CONFIG" ]]; then
  echo "Missing config: $CONFIG" >&2
  exit 1
fi

# Prompt securely only if the key is not already set in this shell.
# The key is exported only to child runner processes, not written to disk and not echoed.
if [[ -z "${XAI_API_KEY:-}" ]]; then
  printf "Enter XAI_API_KEY: " >&2
  IFS= read -r -s XAI_API_KEY
  printf "\n" >&2
  export XAI_API_KEY
  trap 'unset XAI_API_KEY' EXIT
fi

if [[ -z "${XAI_API_KEY:-}" ]]; then
  echo "XAI_API_KEY was empty; aborting." >&2
  exit 1
fi

case "$MODE" in

  firehose|firehose80|firehose160)
    RUN_ID="hosted_clinmap_voi_v0_xai_firehose_${MODE}_$(date -u +%Y%m%dT%H%M%SZ)"
    echo "RUN_ID=$RUN_ID"
    if [[ "$MODE" == "firehose80" ]]; then
      python3 model_runs/run_xai_firehose_clinmap_voi.py         --config "$CONFIG"         --run-id "$RUN_ID"         --models "$MODELS"         --include-supplementary         --full         --limit 80         --rps-per-model "${XAI_RPS_PER_MODEL:-35}"         --concurrency-per-model "${XAI_CONCURRENCY_PER_MODEL:-80}"         --timeout-sec "$TIMEOUT"         --retries "$RETRIES"
    elif [[ "$MODE" == "firehose160" ]]; then
      python3 model_runs/run_xai_firehose_clinmap_voi.py         --config "$CONFIG"         --run-id "$RUN_ID"         --models "$MODELS"         --include-supplementary         --full         --limit 160         --rps-per-model "${XAI_RPS_PER_MODEL:-35}"         --concurrency-per-model "${XAI_CONCURRENCY_PER_MODEL:-80}"         --timeout-sec "$TIMEOUT"         --retries "$RETRIES"
    else
      python3 model_runs/run_xai_firehose_clinmap_voi.py         --config "$CONFIG"         --run-id "$RUN_ID"         --models "$MODELS"         --include-supplementary         --full         --rps-per-model "${XAI_RPS_PER_MODEL:-35}"         --concurrency-per-model "${XAI_CONCURRENCY_PER_MODEL:-80}"         --timeout-sec "$TIMEOUT"         --retries "$RETRIES"
    fi
    ;;

  probe_models)
    python3 model_runs/run_hosted_clinmap_voi.py \
      --config "$CONFIG" \
      --providers xai \
      --include-supplementary \
      --probe-models \
      --timeout-sec "$TIMEOUT"
    ;;

  probe20|probe80|probe160)
    case "$MODE" in
      probe20) LIMIT=20 ;;
      probe80) LIMIT=80 ;;
      probe160) LIMIT=160 ;;
    esac
    RUN_ID="hosted_clinmap_voi_v0_xai_maxrpm_${MODE}_$(date -u +%Y%m%dT%H%M%SZ)"
    echo "RUN_ID=$RUN_ID"
    python3 model_runs/run_hosted_clinmap_voi.py \
      --config "$CONFIG" \
      --run-id "$RUN_ID" \
      --models "$MODELS" \
      --include-supplementary \
      --limit "$LIMIT" \
      --max-workers "$WORKERS" \
      --timeout-sec "$TIMEOUT" \
      --retries "$RETRIES"
    ;;

  turbo)
    # More aggressive than full default: 16 shards by default, all 320 prompts/model.
    # This aims for high effective RPM by increasing concurrency across shards while
    # still leaving per-model client pacing to the config.
    SHARDS="${XAI_SHARDS:-16}"
    RUN_BASE="hosted_clinmap_voi_v0_xai_turbo_$(date -u +%Y%m%dT%H%M%SZ)"
    LOG_DIR="model_runs/outputs/hosted_clinmap_voi_v0/${RUN_BASE}_logs"
    mkdir -p "$LOG_DIR"
    echo "RUN_BASE=$RUN_BASE"
    echo "LOG_DIR=$LOG_DIR"
    echo "Launching TURBO $SHARDS shards × models=[$MODELS] × max-workers=$WORKERS"

    pids=()
    for ((i=0; i<SHARDS; i++)); do
      python3 model_runs/run_hosted_clinmap_voi.py \
        --config "$CONFIG" \
        --run-id "${RUN_BASE}_shard${i}" \
        --models "$MODELS" \
        --include-supplementary \
        --full \
        --shard-index "$i" \
        --shard-count "$SHARDS" \
        --max-workers "$WORKERS" \
        --timeout-sec "$TIMEOUT" \
        --retries "$RETRIES" \
        > "${LOG_DIR}/shard${i}.log" 2>&1 &
      pids+=("$!")
    done

    echo "PIDS=${pids[*]}"
    echo "Monitor with: tail -f ${LOG_DIR}/shard*.log"
    wait "${pids[@]}"
    echo "DONE: $RUN_BASE"
    ;;

  full)
    RUN_BASE="hosted_clinmap_voi_v0_xai_maxrpm_$(date -u +%Y%m%dT%H%M%SZ)"
    LOG_DIR="model_runs/outputs/hosted_clinmap_voi_v0/${RUN_BASE}_logs"
    mkdir -p "$LOG_DIR"
    echo "RUN_BASE=$RUN_BASE"
    echo "LOG_DIR=$LOG_DIR"
    echo "Launching $SHARDS shards × models=[$MODELS] × max-workers=$WORKERS"

    pids=()
    for ((i=0; i<SHARDS; i++)); do
      python3 model_runs/run_hosted_clinmap_voi.py \
        --config "$CONFIG" \
        --run-id "${RUN_BASE}_shard${i}" \
        --models "$MODELS" \
        --include-supplementary \
        --full \
        --shard-index "$i" \
        --shard-count "$SHARDS" \
        --max-workers "$WORKERS" \
        --timeout-sec "$TIMEOUT" \
        --retries "$RETRIES" \
        > "${LOG_DIR}/shard${i}.log" 2>&1 &
      pids+=("$!")
    done

    echo "PIDS=${pids[*]}"
    echo "Monitor with: tail -f ${LOG_DIR}/shard*.log"
    wait "${pids[@]}"
    echo "DONE: $RUN_BASE"
    ;;

  *)
    echo "Usage: $0 [firehose|firehose80|firehose160|probe_models|probe20|probe80|probe160|full|turbo]" >&2
    exit 2
    ;;
esac

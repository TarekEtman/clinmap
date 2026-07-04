#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

CONFIG_BASE="model_runs/hosted_models_clinmap_voi_v0_free_candidates.json"
MODE="${1:-mopup}"            # mopup | smooth30 | probe20
MODELS="${ZAI_MODELS:-zai_glm_4_5_flash_free}"
SHARDS="${ZAI_SHARDS:-3}"
WORKERS="${ZAI_WORKERS:-1}"
RETRIES="${ZAI_RETRIES:-3}"
TIMEOUT="${ZAI_TIMEOUT_SEC:-90}"
RPM_PER_SHARD="${ZAI_RPM_PER_SHARD:-10}"
OUT_DIR="model_runs/outputs/hosted_clinmap_voi_v0"

ensure_zai_env() {
  if [[ -z "${ZAI_API_KEY:-}" ]]; then
    if [[ ! -t 0 ]]; then
      echo "ZAI_API_KEY must be set, or run this script interactively in Terminal." >&2
      exit 1
    fi
    printf "Enter ZAI_API_KEY: " >&2
    IFS= read -r -s ZAI_API_KEY
    printf "\n" >&2
    export ZAI_API_KEY
  fi
  if [[ -z "${ZAI_API_KEY:-}" ]]; then
    echo "ZAI_API_KEY was empty; aborting." >&2
    exit 1
  fi
  trap 'unset ZAI_API_KEY' EXIT
}

write_temp_config() {
  local run_base="$1"
  local tmp_dir="model_runs/tmp/${run_base}"
  mkdir -p "$tmp_dir"
  python3 - <<PY
import json
from pathlib import Path

config_path = Path("${CONFIG_BASE}")
out_path = Path("${tmp_dir}/zai_rpm${RPM_PER_SHARD}_config.json")
models = [m.strip() for m in "${MODELS}".split(",") if m.strip()]
rpm = int("${RPM_PER_SHARD}")

cfg = json.loads(config_path.read_text(encoding="utf-8"))
for model in cfg.get("models", []):
    if model.get("provider") == "zai":
        model["enabled"] = model.get("alias") in models
        if model.get("alias") in models:
            model["rpm"] = rpm

out_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
print(out_path)
PY
}

write_mopup_prompt_pack() {
  local run_base="$1"
  local tmp_dir="model_runs/tmp/${run_base}"
  mkdir -p "$tmp_dir"
  python3 - <<PY
import json
from pathlib import Path

out_dir = Path("${OUT_DIR}")
pack = Path("data/clinmap_voi_v0/model_prompt_pack.jsonl")
all_prompts = [json.loads(l) for l in pack.read_text(encoding="utf-8").splitlines() if l.strip()]
all_ids = {p["prompt_id"] for p in all_prompts}

ok = set()
for p in out_dir.glob("*zai*.jsonl"):
    for l in p.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        r = json.loads(l)
        if (
            r.get("provider") == "zai"
            and r.get("model_alias") == "zai_glm_4_5_flash_free"
            and r.get("status") == "ok"
        ):
            ok.add(r["prompt_id"])

missing_ids = sorted(all_ids - ok)
remaining = [p for p in all_prompts if p["prompt_id"] in missing_ids]
out_path = Path("${tmp_dir}/remaining_prompts.jsonl")
with out_path.open("w", encoding="utf-8") as f:
    for row in remaining:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print(len(remaining))
print(out_path)
PY
}

launch_shards() {
  local run_base="$1"
  local cfg_path="$2"
  local prompt_pack="$3"
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
      --prompt-pack "$prompt_pack" \
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

if [[ ! -f "$CONFIG_BASE" ]]; then
  echo "Missing config: $CONFIG_BASE" >&2
  exit 1
fi

ensure_zai_env

case "$MODE" in
  mopup)
    RUN_BASE="hosted_clinmap_voi_v0_zai_glm45_mopup_$(date -u +%Y%m%dT%H%M%SZ)"
    mop_info="$(write_mopup_prompt_pack "$RUN_BASE")"
    remaining_count="$(printf '%s\n' "$mop_info" | sed -n '1p')"
    prompt_pack="$(printf '%s\n' "$mop_info" | sed -n '2p')"
    if [[ "${remaining_count}" == "0" ]]; then
      echo "Nothing to mop up: Z.AI 4.5 already at 320/320 unique OK."
      exit 0
    fi
    echo "Mopup prompts: ${remaining_count}"
    CFG_PATH="$(write_temp_config "$RUN_BASE")"
    if [[ "${remaining_count}" -le 3 ]]; then
      SHARDS=1
    elif [[ "${remaining_count}" -le 8 ]]; then
      SHARDS=2
    else
      SHARDS="${ZAI_SHARDS:-3}"
    fi
    launch_shards "$RUN_BASE" "$CFG_PATH" "$prompt_pack"
    ;;

  smooth30)
    RUN_BASE="hosted_clinmap_voi_v0_zai_glm45_smooth30_$(date -u +%Y%m%dT%H%M%SZ)"
    CFG_PATH="$(write_temp_config "$RUN_BASE")"
    launch_shards "$RUN_BASE" "$CFG_PATH" "data/clinmap_voi_v0/model_prompt_pack.jsonl"
    ;;

  probe20)
    RUN_ID="hosted_clinmap_voi_v0_zai_glm45_probe20_$(date -u +%Y%m%dT%H%M%SZ)"
    echo "RUN_ID=$RUN_ID"
    python3 model_runs/run_hosted_clinmap_voi.py \
      --config "$CONFIG_BASE" \
      --run-id "$RUN_ID" \
      --models "$MODELS" \
      --include-supplementary \
      --limit 20 \
      --max-workers 3 \
      --timeout-sec "$TIMEOUT" \
      --retries "$RETRIES"
    ;;

  *)
    echo "Usage: $0 [mopup|smooth30|probe20]" >&2
    exit 2
    ;;
esac
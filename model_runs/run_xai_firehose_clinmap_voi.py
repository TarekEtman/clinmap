#!/usr/bin/env python3
"""High-throughput xAI runner for ClinMAP-VOI.

This keeps raw provenance clean by using the normal hosted runner row schema, but
schedules concurrent requests per xAI model with an explicit per-model RPS cap.
No API key is stored or printed; if XAI_API_KEY is absent, it prompts securely.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import getpass
import json
import os
import sys
import threading
import time
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_hosted_clinmap_voi as base  # noqa: E402

DEFAULT_CONFIG = ROOT / "model_runs" / "hosted_models_clinmap_voi_v0_xai_maxrpm.json"
DEFAULT_OUT_DIR = ROOT / "model_runs" / "outputs" / "hosted_clinmap_voi_v0"


def prompt_key_if_needed() -> None:
    if os.environ.get("XAI_API_KEY", "").strip():
        return
    key = getpass.getpass("Enter XAI_API_KEY: ").strip()
    if not key:
        raise SystemExit("XAI_API_KEY was empty; aborting.")
    os.environ["XAI_API_KEY"] = key


def finish_future(
    fut: concurrent.futures.Future[dict[str, Any]],
    output_path: Path,
    write_lock: threading.Lock,
    counts: Counter[str],
    prefix: str,
) -> None:
    try:
        row = fut.result()
    except Exception as exc:  # run_one should already be row-safe; this is a last-resort guard.
        row = {
            "run_id": "unknown",
            "provider": prefix.split("/", 1)[0] if "/" in prefix else "xai",
            "model_alias": prefix.split("/", 1)[1] if "/" in prefix else prefix,
            "model_id": "unknown",
            "prompt_id": "unknown",
            "status": "failed",
            "response_text": "",
            "error": {"type": type(exc).__name__, "body": str(exc)[:2000]},
            "collected_at": base.now_iso(),
            "claim_boundary": "failed firehose row; not scored",
        }
    base.write_jsonl_row(output_path, row, write_lock)
    counts[row.get("status", "unknown")] += 1
    print(
        f"{prefix} completed={sum(counts.values())} prompt={row.get('prompt_id')} status={row.get('status')} retry={row.get('retry_count')}",
        flush=True,
    )


def run_model_firehose(
    provider_name: str,
    provider: dict[str, Any],
    model: dict[str, Any],
    prompts: list[dict[str, Any]],
    output_path: Path,
    write_lock: threading.Lock,
    skip_keys: set[str],
    params: dict[str, Any],
    rps_per_model: float,
    concurrency_per_model: int,
    dry_run: bool,
) -> dict[str, Any]:
    prefix = f"{provider_name}/{model['alias']}"
    planned = len(prompts)
    client = base.make_client(provider, int(params["timeout_sec"]))
    if client is None and not dry_run:
        return {
            "model_alias": model["alias"],
            "provider": provider_name,
            "status": "missing_api_key_or_base_url",
            "planned": planned,
            "ok": 0,
            "failed": planned,
            "skipped": 0,
            "rps_per_model": rps_per_model,
            "concurrency_per_model": concurrency_per_model,
        }

    interval = 1.0 / rps_per_model if rps_per_model > 0 else 0.0
    counts: Counter[str] = Counter()
    skipped = submitted = 0
    futures: set[concurrent.futures.Future[dict[str, Any]]] = set()
    next_start = time.perf_counter()
    started_at = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, concurrency_per_model)) as executor:
        for index, prompt in enumerate(prompts, start=1):
            key = base.task_key(model, prompt)
            if key in skip_keys:
                skipped += 1
                continue
            if dry_run:
                print(f"DRY {prefix} {index}/{planned} {prompt['prompt_id']} rps={rps_per_model}", flush=True)
                counts["dry"] += 1
                continue

            while len(futures) >= concurrency_per_model:
                done, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
                for fut in done:
                    finish_future(fut, output_path, write_lock, counts, prefix)

            now = time.perf_counter()
            if now < next_start:
                time.sleep(next_start - now)
            # Do not catch up after delays; cap starts to roughly rps_per_model.
            next_start = time.perf_counter() + interval

            assert client is not None
            fut = executor.submit(base.run_one, client, provider_name, model, prompt, params, int(params["retries"]))
            futures.add(fut)
            submitted += 1
            print(f"{prefix} submitted={submitted}/{planned - skipped} prompt={prompt['prompt_id']}", flush=True)

        while futures:
            done, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
            for fut in done:
                finish_future(fut, output_path, write_lock, counts, prefix)

    elapsed = max(time.perf_counter() - started_at, 0.001)
    return {
        "model_alias": model["alias"],
        "provider": provider_name,
        "status": "done",
        "planned": planned,
        "submitted": submitted,
        "ok": counts.get("ok", 0),
        "failed": submitted - counts.get("ok", 0),
        "skipped": skipped,
        "status_counts": dict(counts),
        "rps_per_model": rps_per_model,
        "rpm_per_model": rps_per_model * 60,
        "concurrency_per_model": concurrency_per_model,
        "elapsed_sec": round(elapsed, 3),
        "observed_completed_rps": round(sum(counts.values()) / elapsed, 3),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--prompt-pack", type=Path, default=base.PROMPT_PACK)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--models", default="xai_grok_4_3,xai_grok_build_0_1")
    parser.add_argument("--skip-models", default="")
    parser.add_argument("--providers", default="xai")
    parser.add_argument("--include-supplementary", action="store_true", default=True)
    parser.add_argument("--include-disabled", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--split", default="")
    parser.add_argument("--variant-types", default="")
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--top-p", type=float, default=None)
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--timeout-sec", type=int, default=None)
    parser.add_argument("--retries", type=int, default=None)
    parser.add_argument("--retry-failed", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--rps-per-model", type=float, default=35.0, help="Start-rate cap per model. xAI console says 37 RPS; default leaves headroom.")
    parser.add_argument("--concurrency-per-model", type=int, default=80, help="In-flight request cap per model. Needed to sustain high RPS when latency >1s.")
    args = parser.parse_args()

    if args.shard_index < 0 or args.shard_index >= args.shard_count:
        raise SystemExit("--shard-index must be >=0 and < --shard-count")

    config = base.load_config(args.config)
    defaults = config.get("default_params", {})
    args.temperature = defaults.get("temperature", 0) if args.temperature is None else args.temperature
    args.top_p = defaults.get("top_p", 1) if args.top_p is None else args.top_p
    args.max_tokens = defaults.get("max_tokens", 180) if args.max_tokens is None else args.max_tokens
    args.timeout_sec = defaults.get("timeout_sec", 120) if args.timeout_sec is None else args.timeout_sec
    args.retries = defaults.get("retries", 3) if args.retries is None else args.retries

    models = base.selected_models(config, args)
    prompts = base.selected_prompts(args)
    if not models:
        raise SystemExit("No models selected")
    if not prompts:
        raise SystemExit("No prompts selected")

    print(json.dumps({
        "mode": "xai_firehose",
        "models": [f"{m['provider']}/{m['alias']}::{m['model_id']}" for m in models],
        "prompts": len(prompts),
        "planned_requests": len(models) * len(prompts),
        "rps_per_model": args.rps_per_model,
        "rpm_per_model": args.rps_per_model * 60,
        "aggregate_rps_if_all_models": args.rps_per_model * len(models),
        "concurrency_per_model": args.concurrency_per_model,
        "max_tokens": args.max_tokens,
        "retries": args.retries,
        "claim_boundary": "raw xAI hosted model-output corpus only; not scored",
    }, indent=2))
    if args.plan:
        return 0

    if not args.dry_run:
        prompt_key_if_needed()

    run_id = args.run_id or f"hosted_clinmap_voi_v0_xai_firehose_{base.run_stamp()}"
    args.outdir.mkdir(parents=True, exist_ok=True)
    output_path = args.outdir / f"{run_id}.jsonl"
    manifest_path = args.outdir / f"{run_id}_manifest.json"
    skip_keys = base.existing_done(output_path, retry_failed=args.retry_failed)
    params = {
        "run_id": run_id,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "max_tokens": args.max_tokens,
        "timeout_sec": args.timeout_sec,
        "retries": args.retries,
    }

    manifest = {
        "run_id": run_id,
        "runner": str(Path(__file__).resolve()),
        "framework_version": config.get("framework_version", "clinmap-voi-v0.1"),
        "created_at": base.now_iso(),
        "output_path": str(output_path),
        "config_path": str(args.config),
        "prompt_pack": str(args.prompt_pack),
        "providers": sorted({m["provider"] for m in models}),
        "models": [{"alias": m["alias"], "provider": m["provider"], "model_id": m["model_id"]} for m in models],
        "prompt_count": len(prompts),
        "planned_requests": len(models) * len(prompts),
        "already_done_rows": len(skip_keys),
        "rps_per_model": args.rps_per_model,
        "rpm_per_model": args.rps_per_model * 60,
        "concurrency_per_model": args.concurrency_per_model,
        "params": {k: params[k] for k in ["temperature", "top_p", "max_tokens", "timeout_sec", "retries"]},
        "claim_boundary": "Raw hosted xAI model-output corpus only; scoring and clinical claims require separate review.",
        "status": "dry_run" if args.dry_run else "running",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    write_lock = threading.Lock()
    provider_configs = config["providers"]
    summaries = []
    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(models)) as scheduler_executor:
        sched_futures = []
        for model in models:
            provider_name = model["provider"]
            provider = dict(provider_configs[provider_name])
            provider["name"] = provider_name
            sched_futures.append(scheduler_executor.submit(
                run_model_firehose,
                provider_name,
                provider,
                model,
                prompts,
                output_path,
                write_lock,
                skip_keys,
                params,
                args.rps_per_model,
                args.concurrency_per_model,
                args.dry_run,
            ))
        for fut in concurrent.futures.as_completed(sched_futures):
            summary = fut.result()
            summaries.append(summary)
            print(f"SUMMARY {summary}", flush=True)

    elapsed = max(time.perf_counter() - started, 0.001)
    manifest.update({
        "completed_at": base.now_iso(),
        "status": "complete",
        "elapsed_sec": round(elapsed, 3),
        "observed_aggregate_completed_rps": round(sum(s.get("submitted", 0) for s in summaries) / elapsed, 3),
        "worker_summaries": summaries,
    })
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")
    print(f"Wrote {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

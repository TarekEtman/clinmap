#!/usr/bin/env python3
"""Run ClinMAP-VOI v0 prompts against a local Ollama model.

Example:
  python3 model_runs/run_ollama_clinmap_voi.py --model qwen2.5:7b-instruct --limit 16 --dry-run
  python3 model_runs/run_ollama_clinmap_voi.py --model qwen2.5:7b-instruct --limit 40
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROMPT_PACK = ROOT / "data" / "clinmap_voi_v0" / "model_prompt_pack.jsonl"
OUT_DIR = ROOT / "model_runs" / "outputs" / "clinmap_voi_v0"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def short_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def ollama_chat(base_url: str, model: str, system: str, user: str, temperature: float, timeout: int) -> tuple[str, int]:
    url = base_url.rstrip("/") + "/api/chat"
    payload = {
        "model": model,
        "stream": False,
        "options": {"temperature": temperature},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    latency_ms = int((time.perf_counter() - started) * 1000)
    parsed = json.loads(raw)
    return parsed.get("message", {}).get("content", ""), latency_ms


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Ollama model name, e.g. qwen2.5:7b-instruct")
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--prompt-pack", type=Path, default=PROMPT_PACK)
    parser.add_argument("--outdir", type=Path, default=OUT_DIR)
    parser.add_argument("--limit", type=int, default=0, help="0 means all prompts")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--timeout-sec", type=int, default=180)
    parser.add_argument("--sleep-sec", type=float, default=0.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    prompts = read_jsonl(args.prompt_pack)
    selected = prompts[args.offset : args.offset + args.limit if args.limit else None]
    run_id = f"ollama_{args.model.replace('/', '_').replace(':', '_')}_{now_iso().replace(':', '').replace('-', '')}"
    args.outdir.mkdir(parents=True, exist_ok=True)
    output_path = args.outdir / f"{run_id}.jsonl"
    manifest_path = args.outdir / f"{run_id}_manifest.json"

    manifest = {
        "run_id": run_id,
        "framework_version": "clinmap-voi-v0.1",
        "provider": "ollama_local",
        "model_id": args.model,
        "base_url": args.base_url,
        "prompt_pack": str(args.prompt_pack),
        "prompt_count_planned": len(selected),
        "temperature": args.temperature,
        "timeout_sec": args.timeout_sec,
        "dry_run": args.dry_run,
        "started_at": now_iso(),
        "output_path": str(output_path),
    }

    if args.dry_run:
        manifest["status"] = "dry_run_no_requests_sent"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(manifest, indent=2))
        return 0

    ok = 0
    failed = 0
    with output_path.open("w", encoding="utf-8") as out:
        for idx, prompt in enumerate(selected, start=1):
            started = now_iso()
            status = "ok"
            response_text = ""
            latency_ms = None
            error = None
            try:
                response_text, latency_ms = ollama_chat(
                    args.base_url,
                    args.model,
                    prompt["system_prompt"],
                    prompt["user_prompt"],
                    args.temperature,
                    args.timeout_sec,
                )
                ok += 1
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
                status = "failed"
                error = f"{type(exc).__name__}: {exc}"
                failed += 1
            row = {
                "run_id": run_id,
                "framework_version": prompt["framework_version"],
                "provider": "ollama_local",
                "model_id": args.model,
                "variant_id": prompt["variant_id"],
                "family_id": prompt["family_id"],
                "prompt_id": prompt["prompt_id"],
                "prompt_hash": prompt["prompt_hash"],
                "expected_policy_label": prompt["expected_policy_label"],
                "risk_stratum": prompt["risk_stratum"],
                "metamorphic_relation": prompt["metamorphic_relation"],
                "status": status,
                "response_text": response_text,
                "response_hash": short_hash(response_text) if response_text else "",
                "latency_ms": latency_ms,
                "collected_at": started,
                "error": error,
                "temperature": args.temperature,
            }
            out.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            print(f"[{idx}/{len(selected)}] {prompt['variant_id']} {status}")
            if args.sleep_sec:
                time.sleep(args.sleep_sec)

    manifest.update({"status": "complete" if failed == 0 else "partial_collection", "completed_at": now_iso(), "ok": ok, "failed": failed})
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")
    print(f"Wrote {manifest_path}")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Quota-aware, resumable hosted API runner for ClinMAP-VOI v0.

No API keys are stored. Set provider keys with environment variables:
  GROQ_API_KEY
  CEREBRAS_API_KEY
  MISTRAL_API_KEY

Examples:
  python3 model_runs/run_hosted_clinmap_voi.py --plan --limit 1
  python3 model_runs/run_hosted_clinmap_voi.py --probe-models
  python3 model_runs/run_hosted_clinmap_voi.py --limit 16 --models groq_qwen3_6_27b,cerebras_gpt_oss_120b
  python3 model_runs/run_hosted_clinmap_voi.py --full --max-workers 12
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import random
import re
import threading
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROMPT_PACK = ROOT / "data" / "clinmap_voi_v0" / "model_prompt_pack.jsonl"
VARIANTS = ROOT / "data" / "clinmap_voi_v0" / "variants.jsonl"
CONFIG = ROOT / "model_runs" / "hosted_models_clinmap_voi_v0.json"
OUT_DIR = ROOT / "model_runs" / "outputs" / "hosted_clinmap_voi_v0"

SENSITIVE_HEADER_PREFIXES = ("authorization", "cookie", "set-cookie")
RATE_HEADER_PREFIXES = ("x-ratelimit", "retry-after", "ratelimit")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def short_hash(text: str, n: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl_row(path: Path, row: dict[str, Any], lock: threading.Lock) -> None:
    with lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            f.flush()


def safe_headers(headers: Any) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in dict(headers).items():
        lower = key.lower()
        if lower.startswith(SENSITIVE_HEADER_PREFIXES):
            continue
        if lower.startswith(RATE_HEADER_PREFIXES):
            result[key] = str(value)
    return result


def load_config(path: Path = CONFIG) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def selected_prompts(args: argparse.Namespace) -> list[dict[str, Any]]:
    prompts = read_jsonl(args.prompt_pack)
    if args.split:
        variant_by_id = {v["variant_id"]: v for v in read_jsonl(VARIANTS)}
        prompts = [p for p in prompts if variant_by_id[p["variant_id"]].get("split") == args.split]
    if args.variant_types:
        allowed = set(args.variant_types.split(","))
        variant_by_id = {v["variant_id"]: v for v in read_jsonl(VARIANTS)}
        prompts = [p for p in prompts if variant_by_id[p["variant_id"]].get("variant_type") in allowed]
    if args.shard_count > 1:
        prompts = [p for i, p in enumerate(prompts) if i % args.shard_count == args.shard_index]
    if args.offset:
        prompts = prompts[args.offset :]
    if args.limit:
        prompts = prompts[: args.limit]
    return prompts


def resolve_model_entry(model: dict[str, Any]) -> dict[str, Any] | None:
    resolved = dict(model)
    model_id_env = resolved.get("model_id_env")
    if model_id_env:
        env_value = os.environ.get(model_id_env, "").strip()
        if env_value:
            resolved["model_id"] = env_value
            resolved["enabled"] = True
        elif not resolved.get("model_id") or str(resolved.get("model_id", "")).startswith("<"):
            return None
    if not resolved.get("model_id") or str(resolved.get("model_id", "")).startswith("<"):
        return None
    return resolved


def selected_models(config: dict[str, Any], args: argparse.Namespace) -> list[dict[str, Any]]:
    explicit_selection = bool(args.providers or args.models)
    models = []
    for raw in config["models"]:
        env_model_is_set = bool(raw.get("model_id_env") and os.environ.get(str(raw.get("model_id_env")), "").strip())
        if raw.get("enabled", True) is False and not args.include_disabled and not env_model_is_set:
            continue
        if raw.get("status") == "supplementary" and not (args.include_supplementary or explicit_selection):
            continue
        resolved = resolve_model_entry(raw)
        if resolved is None:
            if args.include_disabled:
                models.append(dict(raw))
            continue
        models.append(resolved)
    if args.providers:
        providers = set(args.providers.split(","))
        models = [m for m in models if m["provider"] in providers]
    if args.models:
        requested = set(args.models.split(","))
        models = [m for m in models if m["alias"] in requested or m.get("model_id") in requested]
    if args.skip_models:
        skipped = set(args.skip_models.split(","))
        models = [m for m in models if m["alias"] not in skipped and m.get("model_id") not in skipped]
    models.sort(key=lambda m: (m.get("priority", 999), m["provider"], m["alias"]))
    return models

def task_key(model: dict[str, Any], prompt: dict[str, Any]) -> str:
    return f"{model['provider']}::{model['model_id']}::{prompt['prompt_id']}"


def existing_done(path: Path, retry_failed: bool = False) -> set[str]:
    if not path.exists():
        return set()
    done: set[str] = set()
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            status = row.get("status")
            if status == "ok" or (status and not retry_failed):
                done.add(f"{row.get('provider')}::{row.get('model_id')}::{row.get('prompt_id')}")
    return done


@dataclass
class ProviderClient:
    provider_name: str
    base_url: str
    api_key: str
    timeout_sec: int

    def _request(self, path: str, payload: dict[str, Any] | None = None, method: str = "POST") -> tuple[dict[str, Any], dict[str, str], int]:
        url = self.base_url.rstrip("/") + path
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "User-Agent": "clinmap-voi-eval/0.1",
        }
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        if body is not None:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        started = time.perf_counter()
        with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
            raw = resp.read().decode("utf-8")
            latency_ms = int((time.perf_counter() - started) * 1000)
            return json.loads(raw), safe_headers(resp.headers), latency_ms

    def list_models(self) -> tuple[list[str], dict[str, str], int]:
        data, headers, latency_ms = self._request("/models", payload=None, method="GET")
        ids = [item.get("id", "") for item in data.get("data", []) if item.get("id")]
        return sorted(ids), headers, latency_ms

    def chat(self, model_id: str, system_prompt: str, user_prompt: str, params: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str], int]:
        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": params["temperature"],
            "top_p": params["top_p"],
            "max_tokens": params["max_tokens"],
        }
        return self._request("/chat/completions", payload=payload, method="POST")


def make_client(provider: dict[str, Any], timeout_sec: int) -> ProviderClient | None:
    api_key = os.environ.get(provider.get("api_key_env", ""), "").strip()
    if not api_key:
        for env_name in provider.get("api_key_envs", []):
            api_key = os.environ.get(env_name, "").strip()
            if api_key:
                break
    if not api_key:
        return None
    base_url = provider.get("base_url", "")
    base_url_env = provider.get("base_url_env")
    if base_url_env and os.environ.get(base_url_env):
        base_url = os.environ[base_url_env]
    if not base_url or str(base_url).startswith("<"):
        return None
    return ProviderClient(provider_name=provider.get("name", ""), base_url=base_url, api_key=api_key, timeout_sec=timeout_sec)


def parse_chat_response(data: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    choice = (data.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    content = message.get("content") or choice.get("text") or ""
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                value = item.get("text") or item.get("content") or item.get("output_text")
                if isinstance(value, str):
                    parts.append(value)
                elif value is not None:
                    parts.append(json.dumps(value, ensure_ascii=False, sort_keys=True))
            elif item is not None:
                parts.append(str(item))
        text = "\n".join(part for part in parts if part)
    elif isinstance(content, str):
        text = content
    elif content is None:
        text = ""
    else:
        text = str(content)
    meta = {
        "finish_reason": choice.get("finish_reason"),
        "usage": data.get("usage", {}),
        "response_id": data.get("id"),
        "created": data.get("created"),
    }
    return text, meta


def retry_delay(exc: Exception, attempt: int, headers: dict[str, str] | None = None, body: str = "") -> float:
    if headers:
        for key, value in headers.items():
            if key.lower() == "retry-after":
                try:
                    return max(float(value), 1.0)
                except ValueError:
                    pass
    if body:
        for pattern in (r'"retryDelay"\s*:\s*"([0-9.]+)s"', r"Please retry in ([0-9.]+)s"):
            match = re.search(pattern, body)
            if match:
                try:
                    return max(float(match.group(1)), 1.0) + random.random()
                except ValueError:
                    pass
    base = min(2 ** attempt, 30)
    return base + random.random()


def run_one(client: ProviderClient, provider_name: str, model: dict[str, Any], prompt: dict[str, Any], params: dict[str, Any], retries: int) -> dict[str, Any]:
    collected_at = now_iso()
    last_error = None
    rate_headers: dict[str, str] = {}
    for attempt in range(retries + 1):
        try:
            data, headers, latency_ms = client.chat(model["model_id"], prompt["system_prompt"], prompt["user_prompt"], params)
            text, meta = parse_chat_response(data)
            return {
                "run_id": params["run_id"],
                "framework_version": prompt["framework_version"],
                "provider": provider_name,
                "model_alias": model["alias"],
                "model_id": model["model_id"],
                "prompt_id": prompt["prompt_id"],
                "variant_id": prompt["variant_id"],
                "family_id": prompt["family_id"],
                "prompt_hash": prompt["prompt_hash"],
                "expected_policy_label": prompt["expected_policy_label"],
                "risk_stratum": prompt["risk_stratum"],
                "metamorphic_relation": prompt["metamorphic_relation"],
                "status": "ok",
                "response_text": text,
                "response_hash": short_hash(text) if text else "",
                "latency_ms": latency_ms,
                "retry_count": attempt,
                "temperature": params["temperature"],
                "top_p": params["top_p"],
                "max_tokens": params["max_tokens"],
                "finish_reason": meta.get("finish_reason"),
                "usage": meta.get("usage", {}),
                "provider_response_id": meta.get("response_id"),
                "provider_created": meta.get("created"),
                "rate_limit_headers": headers,
                "collected_at": collected_at,
                "redaction_status": "not_needed_synthetic_prompt",
                "claim_boundary": "raw model output only; not scored and not clinical validation",
            }
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:2000]
            rate_headers = safe_headers(exc.headers)
            last_error = {"type": "HTTPError", "code": exc.code, "reason": exc.reason, "body": body}
            if exc.code in {408, 409, 425, 429, 500, 502, 503, 504} and attempt < retries:
                time.sleep(retry_delay(exc, attempt, rate_headers, body))
                continue
            break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
            last_error = {"type": type(exc).__name__, "body": str(exc)[:2000]}
            if attempt < retries:
                time.sleep(retry_delay(exc, attempt))
                continue
            break
        except Exception as exc:  # keep row-level collection resumable on provider/client edge cases
            last_error = {"type": type(exc).__name__, "body": str(exc)[:2000]}
            if attempt < retries:
                time.sleep(retry_delay(exc, attempt))
                continue
            break
    status = "failed"
    if isinstance(last_error, dict) and last_error.get("code") == 429:
        status = "rate_limited"
    return {
        "run_id": params["run_id"],
        "framework_version": prompt["framework_version"],
        "provider": provider_name,
        "model_alias": model["alias"],
        "model_id": model["model_id"],
        "prompt_id": prompt["prompt_id"],
        "variant_id": prompt["variant_id"],
        "family_id": prompt["family_id"],
        "prompt_hash": prompt["prompt_hash"],
        "expected_policy_label": prompt["expected_policy_label"],
        "risk_stratum": prompt["risk_stratum"],
        "metamorphic_relation": prompt["metamorphic_relation"],
        "status": status,
        "response_text": "",
        "response_hash": "",
        "latency_ms": None,
        "retry_count": retries,
        "temperature": params["temperature"],
        "top_p": params["top_p"],
        "max_tokens": params["max_tokens"],
        "finish_reason": None,
        "usage": {},
        "rate_limit_headers": rate_headers,
        "error": last_error,
        "collected_at": collected_at,
        "redaction_status": "not_needed_synthetic_prompt",
        "claim_boundary": "failed raw model-output collection row; not scored",
    }


def run_model_worker(
    provider_name: str,
    provider: dict[str, Any],
    model: dict[str, Any],
    prompts: list[dict[str, Any]],
    output_path: Path,
    write_lock: threading.Lock,
    skip_keys: set[str],
    params: dict[str, Any],
    dry_run: bool = False,
) -> dict[str, Any]:
    rpm = float(model.get("rpm") or provider.get("default_rpm_per_model") or 30)
    min_interval = 60.0 / rpm if rpm > 0 else 0.0
    client = make_client(provider, int(params["timeout_sec"]))
    if client is None and not dry_run:
        return {"model_alias": model["alias"], "provider": provider_name, "status": "missing_api_key_or_base_url", "planned": len(prompts), "ok": 0, "failed": len(prompts), "skipped": 0}
    ok = failed = skipped = 0
    last_start = 0.0
    for index, prompt in enumerate(prompts, start=1):
        key = task_key(model, prompt)
        if key in skip_keys:
            skipped += 1
            continue
        if dry_run:
            print(f"DRY {provider_name}/{model['alias']} {index}/{len(prompts)} {prompt['prompt_id']}")
            continue
        elapsed = time.perf_counter() - last_start
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        last_start = time.perf_counter()
        assert client is not None
        row = run_one(client, provider_name, model, prompt, params, int(params["retries"]))
        write_jsonl_row(output_path, row, write_lock)
        if row["status"] == "ok":
            ok += 1
        else:
            failed += 1
        print(f"{provider_name}/{model['alias']} {index}/{len(prompts)} {prompt['prompt_id']} {row['status']}")
    return {"model_alias": model["alias"], "provider": provider_name, "status": "done", "planned": len(prompts), "ok": ok, "failed": failed, "skipped": skipped}


def probe_models(config: dict[str, Any], timeout_sec: int) -> dict[str, Any]:
    report: dict[str, Any] = {"created_at": now_iso(), "providers": {}, "configured_model_checks": []}
    providers = config["providers"]
    for provider_name, provider in providers.items():
        client = make_client(provider, timeout_sec)
        if client is None:
            report["providers"][provider_name] = {"status": "missing_api_key_or_base_url", "api_key_env": provider["api_key_env"], "models": []}
            continue
        try:
            ids, headers, latency_ms = client.list_models()
            report["providers"][provider_name] = {"status": "ok", "model_count": len(ids), "models": ids, "latency_ms": latency_ms, "rate_limit_headers": headers}
        except Exception as exc:  # intentionally broad for probe report
            report["providers"][provider_name] = {"status": "failed", "error": f"{type(exc).__name__}: {exc}", "models": []}
    available_by_provider = {name: set(info.get("models", [])) for name, info in report["providers"].items()}
    for model in config["models"]:
        model_id = model["model_id"]
        provider_ids = available_by_provider.get(model["provider"], set())
        available = model_id in provider_ids or f"models/{model_id}" in provider_ids
        report["configured_model_checks"].append({**model, "available_in_probe": available})
    return report


def print_plan(models: list[dict[str, Any]], prompts: list[dict[str, Any]], args: argparse.Namespace) -> None:
    by_provider = Counter(m["provider"] for m in models)
    planned = len(models) * len(prompts)
    print(json.dumps({
        "planned_requests": planned,
        "models": len(models),
        "prompts": len(prompts),
        "providers": dict(by_provider),
        "limit": args.limit,
        "split": args.split,
        "shard_index": args.shard_index,
        "shard_count": args.shard_count,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "max_tokens": args.max_tokens,
    }, indent=2))
    for model in models:
        print(f"- {model['provider']}/{model['alias']} :: {model['model_id']} rpm={model.get('rpm')}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--prompt-pack", type=Path, default=PROMPT_PACK)
    parser.add_argument("--outdir", type=Path, default=OUT_DIR)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--models", default="", help="Comma-separated aliases or model IDs")
    parser.add_argument("--skip-models", default="", help="Comma-separated aliases or model IDs")
    parser.add_argument("--providers", default="", help="Comma-separated provider names")
    parser.add_argument("--include-supplementary", action="store_true", help="Include supplementary providers/models such as Google/NVIDIA. Default run is core only.")
    parser.add_argument("--include-disabled", action="store_true", help="Include disabled placeholder models for planning/debugging only.")
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
    parser.add_argument("--max-workers", type=int, default=12)
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--probe-models", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--retry-failed", action="store_true")
    parser.add_argument("--full", action="store_true", help="Alias for no prompt limit; included for explicitness")
    args = parser.parse_args()

    if args.shard_index < 0 or args.shard_index >= args.shard_count:
        raise SystemExit("--shard-index must be >=0 and < --shard-count")

    config = load_config(args.config)
    defaults = config.get("default_params", {})
    args.temperature = defaults.get("temperature", 0) if args.temperature is None else args.temperature
    args.top_p = defaults.get("top_p", 1) if args.top_p is None else args.top_p
    args.max_tokens = defaults.get("max_tokens", 180) if args.max_tokens is None else args.max_tokens
    args.timeout_sec = defaults.get("timeout_sec", 120) if args.timeout_sec is None else args.timeout_sec
    args.retries = defaults.get("retries", 3) if args.retries is None else args.retries

    models = selected_models(config, args)
    prompts = selected_prompts(args)
    if not models:
        raise SystemExit("No models selected")
    if not prompts:
        raise SystemExit("No prompts selected")

    if args.probe_models:
        report = probe_models(config, int(args.timeout_sec))
        args.outdir.mkdir(parents=True, exist_ok=True)
        path = args.outdir / f"provider_model_probe_{run_stamp()}.json"
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"probe_report": str(path)}, indent=2))
        for check in report["configured_model_checks"]:
            marker = "OK" if check["available_in_probe"] else "MISS"
            print(f"{marker} {check['provider']}/{check['alias']} {check['model_id']}")
        return 0

    print_plan(models, prompts, args)
    if args.plan:
        return 0

    run_id = args.run_id or f"hosted_clinmap_voi_v0_{run_stamp()}"
    args.outdir.mkdir(parents=True, exist_ok=True)
    output_path = args.outdir / f"{run_id}.jsonl"
    manifest_path = args.outdir / f"{run_id}_manifest.json"
    skip_keys = existing_done(output_path, retry_failed=args.retry_failed)
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
        "framework_version": config.get("framework_version", "clinmap-voi-v0.1"),
        "created_at": now_iso(),
        "output_path": str(output_path),
        "config_path": str(args.config),
        "prompt_pack": str(args.prompt_pack),
        "providers": sorted({m["provider"] for m in models}),
        "models": [{"alias": m["alias"], "provider": m["provider"], "model_id": m["model_id"], "rpm": m.get("rpm")} for m in models],
        "prompt_count": len(prompts),
        "planned_requests": len(models) * len(prompts),
        "include_supplementary": args.include_supplementary,
        "already_done_rows": len(skip_keys),
        "params": {k: params[k] for k in ["temperature", "top_p", "max_tokens", "timeout_sec", "retries"]},
        "claim_boundary": "Raw hosted model-output corpus only; scoring and clinical claims require separate review.",
        "status": "dry_run" if args.dry_run else "running",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    write_lock = threading.Lock()
    provider_configs = config["providers"]
    worker_count = min(max(1, args.max_workers), len(models))
    summaries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = []
        for model in models:
            provider_name = model["provider"]
            provider = dict(provider_configs[provider_name])
            provider["name"] = provider_name
            futures.append(
                executor.submit(
                    run_model_worker,
                    provider_name,
                    provider,
                    model,
                    prompts,
                    output_path,
                    write_lock,
                    skip_keys,
                    params,
                    args.dry_run,
                )
            )
        for future in concurrent.futures.as_completed(futures):
            summary = future.result()
            summaries.append(summary)
            print(f"SUMMARY {summary}")

    manifest.update({"completed_at": now_iso(), "status": "complete", "worker_summaries": summaries})
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")
    print(f"Wrote {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

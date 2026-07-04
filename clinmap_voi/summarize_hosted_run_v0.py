#!/usr/bin/env python3
"""Summarize hosted ClinMAP-VOI model-output corpus runs."""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clinmap_voi.common import ROOT, read_jsonl  # noqa: E402

OUT_DIR = ROOT / "report" / "hosted_runs"


def numeric(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def usage_sum(rows: list[dict[str, Any]]) -> dict[str, int]:
    total = Counter()
    for row in rows:
        usage = row.get("usage") or {}
        for key in ["prompt_tokens", "completion_tokens", "total_tokens", "input_tokens", "output_tokens"]:
            value = usage.get(key)
            if isinstance(value, int):
                total[key] += value
    return dict(total)


def summarize(path: Path) -> dict[str, Any]:
    rows = read_jsonl(path)
    ok_rows = [r for r in rows if r.get("status") == "ok"]
    latencies = [numeric(r.get("latency_ms")) for r in ok_rows]
    latencies = [v for v in latencies if v is not None]
    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_provider: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_model[f"{row.get('provider')}/{row.get('model_alias')}"].append(row)
        by_provider[str(row.get("provider"))].append(row)

    model_summary = {}
    for model, model_rows in sorted(by_model.items()):
        model_ok = [r for r in model_rows if r.get("status") == "ok"]
        model_latencies = [numeric(r.get("latency_ms")) for r in model_ok]
        model_latencies = [v for v in model_latencies if v is not None]
        model_summary[model] = {
            "rows": len(model_rows),
            "status_counts": dict(Counter(str(r.get("status")) for r in model_rows)),
            "unique_families": len({r.get("family_id") for r in model_rows}),
            "unique_variants": len({r.get("variant_id") for r in model_rows}),
            "mean_latency_ms": round(statistics.mean(model_latencies), 2) if model_latencies else None,
            "p95_latency_ms": round(sorted(model_latencies)[int(0.95 * (len(model_latencies) - 1))], 2) if model_latencies else None,
            "usage": usage_sum(model_rows),
        }

    provider_summary = {}
    for provider, provider_rows in sorted(by_provider.items()):
        provider_summary[provider] = {
            "rows": len(provider_rows),
            "status_counts": dict(Counter(str(r.get("status")) for r in provider_rows)),
            "models": sorted({r.get("model_alias") for r in provider_rows}),
            "usage": usage_sum(provider_rows),
        }

    return {
        "source_path": str(path),
        "row_count": len(rows),
        "ok_count": len(ok_rows),
        "status_counts": dict(Counter(str(r.get("status")) for r in rows)),
        "providers": provider_summary,
        "models": model_summary,
        "unique_prompts": len({r.get("prompt_id") for r in rows}),
        "unique_families": len({r.get("family_id") for r in rows}),
        "unique_variants": len({r.get("variant_id") for r in rows}),
        "mean_latency_ms": round(statistics.mean(latencies), 2) if latencies else None,
        "p95_latency_ms": round(sorted(latencies)[int(0.95 * (len(latencies) - 1))], 2) if latencies else None,
        "usage": usage_sum(rows),
        "claim_boundary": "Raw hosted model-output corpus summary only. This is not scoring, clinical validation, or a model-safety claim.",
    }


def write_markdown(summary: dict[str, Any], path: Path) -> None:
    lines = [
        "# ClinMAP-VOI Hosted Run Summary",
        "",
        f"Source: `{summary['source_path']}`",
        "",
        "This is a raw hosted model-output corpus summary. It is not scoring, clinical validation, or a model-safety claim.",
        "",
        "## Corpus counts",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| rows | {summary['row_count']} |",
        f"| ok rows | {summary['ok_count']} |",
        f"| unique prompts | {summary['unique_prompts']} |",
        f"| unique families | {summary['unique_families']} |",
        f"| unique variants | {summary['unique_variants']} |",
        f"| mean latency ms | {summary['mean_latency_ms']} |",
        f"| p95 latency ms | {summary['p95_latency_ms']} |",
        "",
        "## Status counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in sorted(summary["status_counts"].items()):
        lines.append(f"| {status} | {count} |")
    lines.extend(["", "## Provider summary", "", "| Provider | Rows | Status counts | Models |", "|---|---:|---|---|"])
    for provider, info in summary["providers"].items():
        lines.append(f"| {provider} | {info['rows']} | `{json.dumps(info['status_counts'], sort_keys=True)}` | {', '.join(info['models'])} |")
    lines.extend(["", "## Model summary", "", "| Model | Rows | Status counts | Mean latency ms | Usage |", "|---|---:|---|---:|---|"])
    for model, info in summary["models"].items():
        lines.append(f"| {model} | {info['rows']} | `{json.dumps(info['status_counts'], sort_keys=True)}` | {info['mean_latency_ms']} | `{json.dumps(info['usage'], sort_keys=True)}` |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_jsonl", type=Path)
    parser.add_argument("--outdir", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    summary = summarize(args.run_jsonl)
    args.outdir.mkdir(parents=True, exist_ok=True)
    stem = args.run_jsonl.stem
    json_path = args.outdir / f"{stem}_summary.json"
    md_path = args.outdir / f"{stem}_summary.md"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(summary, md_path)
    print(json_path)
    print(md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

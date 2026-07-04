"""CLI for the Clinical Model Behavior Evaluation Lab."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print("$ " + " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(prog="cmb-eval", description="Clinical Model Behavior Evaluation Lab CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build-data")
    sub.add_parser("validate")
    sub.add_parser("schema-validate")
    sub.add_parser("metrics")
    sub.add_parser("report")
    sub.add_parser("charts")
    sub.add_parser("export-openai")
    sub.add_parser("audit")
    args = parser.parse_args()
    py = sys.executable
    commands = {
        "build-data": [py, "eval_harness/build_v1_demo_dataset.py"],
        "validate": [py, "eval_harness/v1_validate.py"],
        "schema-validate": [py, "eval_harness/v1_schema_validate.py"],
        "metrics": [py, "eval_harness/v1_metrics.py"],
        "report": [py, "eval_harness/v1_generate_report.py"],
        "charts": [py, "eval_harness/v1_generate_charts.py"],
        "export-openai": [py, "adapters/openai_evals/export_v1_openai_evals.py"],
        "audit": ["make", "audit"],
    }
    return run(commands[args.cmd])


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate synthetic cases and summarize scored examples.

Usage:
    python3 eval_harness/run_eval.py \
      --cases data/synthetic_cases.jsonl \
      --scores data/scored_examples.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from scoring_schema import (
    FAILURE_MODE_LABELS,
    REQUIRED_CASE_FIELDS,
    REQUIRED_SCORE_FIELDS,
    VALID_PASS_FAIL,
    VALID_RESPONSE_LABELS,
    VALID_SEVERITIES,
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON on line {line_no}: {exc}") from exc
    return rows


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def validate_cases(cases: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for idx, case in enumerate(cases, start=1):
        missing = REQUIRED_CASE_FIELDS - set(case)
        if missing:
            errors.append(f"case row {idx} missing fields: {sorted(missing)}")
        case_id = case.get("case_id")
        if case_id in seen:
            errors.append(f"duplicate case_id: {case_id}")
        seen.add(case_id)
        if case.get("preferred_response") not in VALID_RESPONSE_LABELS:
            errors.append(f"{case_id}: preferred_response must be A or B")
        for list_field in ["expected_behavior", "unsafe_behaviors", "tags"]:
            if list_field in case and not isinstance(case[list_field], list):
                errors.append(f"{case_id}: {list_field} must be a list")
    return errors


def validate_scores(scores: list[dict[str, str]], case_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for idx, row in enumerate(scores, start=1):
        missing = REQUIRED_SCORE_FIELDS - set(row)
        if missing:
            errors.append(f"score row {idx} missing fields: {sorted(missing)}")
            continue
        case_id = row["case_id"]
        if case_id not in case_ids:
            errors.append(f"score row {idx}: unknown case_id {case_id}")
        if row["response_label"] not in VALID_RESPONSE_LABELS:
            errors.append(f"{case_id}: response_label must be A or B")
        if row["pass_fail"] not in VALID_PASS_FAIL:
            errors.append(f"{case_id}: pass_fail must be one of {sorted(VALID_PASS_FAIL)}")
        if row["severity"] not in VALID_SEVERITIES:
            errors.append(f"{case_id}: severity must be 0-4")
        for score_field in ["primary_score", "secondary_score"]:
            try:
                score = int(row[score_field])
            except ValueError:
                errors.append(f"{case_id}: {score_field} must be integer")
                continue
            if score < 0 or score > 4:
                errors.append(f"{case_id}: {score_field} must be 0-4")
    return errors


def split_failure_tags(raw: str) -> list[str]:
    if not raw.strip():
        return []
    return [tag.strip() for tag in raw.split(";") if tag.strip()]


def summarize(cases: list[dict[str, Any]], scores: list[dict[str, str]]) -> str:
    category_counts = Counter(case["category"] for case in cases)
    risk_counts = Counter(case["clinical_risk_level"] for case in cases)
    pass_counts = Counter(row["pass_fail"] for row in scores)
    severity_counts = Counter(row["severity"] for row in scores)
    failure_counts: Counter[str] = Counter()
    primary_scores: list[int] = []
    secondary_scores: list[int] = []
    by_case: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in scores:
        primary_scores.append(int(row["primary_score"]))
        secondary_scores.append(int(row["secondary_score"]))
        by_case[row["case_id"]].append(row)
        for tag in split_failure_tags(row["failure_tags"]):
            failure_counts[tag] += 1

    preferred_lookup = {case["case_id"]: case["preferred_response"] for case in cases}
    preferred_pass = 0
    preferred_total = 0
    for case_id, rows in by_case.items():
        preferred = preferred_lookup.get(case_id)
        for row in rows:
            if row["response_label"] == preferred:
                preferred_total += 1
                if row["pass_fail"] == "pass":
                    preferred_pass += 1

    unknown_failure_tags = [tag for tag in failure_counts if tag not in FAILURE_MODE_LABELS]

    lines = []
    lines.append("Clinical Model Evaluation Systems Lab - demonstration summary")
    lines.append("=" * 60)
    lines.append(f"Cases: {len(cases)}")
    lines.append(f"Scored response records: {len(scores)}")
    lines.append(f"Mean primary score: {mean(primary_scores):.2f} / 4")
    lines.append(f"Mean secondary score: {mean(secondary_scores):.2f} / 4")
    if preferred_total:
        lines.append(f"Preferred-response pass rate: {preferred_pass}/{preferred_total} ({preferred_pass / preferred_total:.0%})")
    lines.append("")
    lines.append("Case categories:")
    for category, count in sorted(category_counts.items()):
        lines.append(f"  - {category}: {count}")
    lines.append("")
    lines.append("Risk levels:")
    for risk, count in sorted(risk_counts.items()):
        lines.append(f"  - {risk}: {count}")
    lines.append("")
    lines.append("Pass/fail distribution:")
    for status, count in sorted(pass_counts.items()):
        lines.append(f"  - {status}: {count}")
    lines.append("")
    lines.append("Severity distribution:")
    for severity, count in sorted(severity_counts.items()):
        lines.append(f"  - {severity}: {count}")
    lines.append("")
    lines.append("Failure tag frequency:")
    for tag, count in failure_counts.most_common():
        label = FAILURE_MODE_LABELS.get(tag, "UNKNOWN")
        lines.append(f"  - {tag} ({label}): {count}")
    if unknown_failure_tags:
        lines.append("")
        lines.append(f"WARNING: unknown failure tags: {', '.join(sorted(unknown_failure_tags))}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--scores", required=True, type=Path)
    args = parser.parse_args()

    cases = load_jsonl(args.cases)
    scores = load_csv(args.scores)
    case_errors = validate_cases(cases)
    score_errors = validate_scores(scores, {case["case_id"] for case in cases})
    errors = case_errors + score_errors
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)
    print(summarize(cases, scores))


if __name__ == "__main__":
    main()

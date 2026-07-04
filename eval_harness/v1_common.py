"""Shared helpers for v1 synthetic evaluation data."""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "data" / "v1"

DIMENSIONS = [
    "clinical_safety",
    "escalation",
    "context_sensitivity",
    "factuality",
    "uncertainty",
    "scope_control",
    "usefulness",
    "rationale_quality",
]

FAILURE_TAGS = {"FR", "EO", "CQ", "MS", "HF", "SC", "RF", "OR", "EU", "SN"}
RESPONSE_ORIGINS = {"actual_model_output", "synthetic_model_pattern", "human_baseline", "expert_ideal"}
PASS_FAIL = {"pass", "review", "fail"}
RISK_LEVELS = {"low", "medium", "medium_high", "high", "critical"}
CALIBRATION_ROLES = {"high_risk_positive", "low_acuity_control", "borderline", "over_refusal_control", "factuality_control", "reasoning_control"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return rows


def load_v1(base: Path = V1) -> dict[str, Any]:
    manifest_path = base / "dataset_manifest.json"
    run_manifest_path = base / "run_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    run_manifest = json.loads(run_manifest_path.read_text(encoding="utf-8")) if run_manifest_path.exists() else {}
    return {
        "base": base,
        "manifest": manifest,
        "run_manifest": run_manifest,
        "source_anchors": read_jsonl(base / "source_anchors.jsonl"),
        "cases": read_jsonl(base / "cases.jsonl"),
        "responses": read_jsonl(base / "responses.jsonl"),
        "annotations": read_jsonl(base / "annotations.jsonl"),
        "adjudications": read_jsonl(base / "adjudications.jsonl"),
        "preferences": read_jsonl(base / "pairwise_preferences.jsonl"),
    }


def counter(rows: Iterable[dict[str, Any]], field: str) -> Counter:
    return Counter(str(row.get(field, "")) for row in rows)


def group_by(rows: Iterable[dict[str, Any]], field: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(field, ""))].append(row)
    return dict(grouped)


def quadratic_weighted_kappa(pairs: list[tuple[int, int]], min_rating: int = 0, max_rating: int = 4) -> float | None:
    if not pairs:
        return None
    n_ratings = max_rating - min_rating + 1
    observed = [[0.0 for _ in range(n_ratings)] for _ in range(n_ratings)]
    hist_a = [0.0 for _ in range(n_ratings)]
    hist_b = [0.0 for _ in range(n_ratings)]
    for a, b in pairs:
        ia, ib = a - min_rating, b - min_rating
        observed[ia][ib] += 1
        hist_a[ia] += 1
        hist_b[ib] += 1
    n = float(len(pairs))
    expected = [[hist_a[i] * hist_b[j] / n for j in range(n_ratings)] for i in range(n_ratings)]
    denom_scale = (n_ratings - 1) ** 2
    weighted_observed = 0.0
    weighted_expected = 0.0
    for i in range(n_ratings):
        for j in range(n_ratings):
            w = ((i - j) ** 2) / denom_scale
            weighted_observed += w * observed[i][j]
            weighted_expected += w * expected[i][j]
    if weighted_expected == 0:
        return 1.0
    return round(1.0 - weighted_observed / weighted_expected, 4)


def cohen_kappa(labels: list[tuple[str, str]]) -> float | None:
    if not labels:
        return None
    total = len(labels)
    observed = sum(1 for a, b in labels if a == b) / total
    counts_a = Counter(a for a, _ in labels)
    counts_b = Counter(b for _, b in labels)
    expected = sum((counts_a[k] / total) * (counts_b[k] / total) for k in set(counts_a) | set(counts_b))
    if expected == 1:
        return 1.0
    return round((observed - expected) / (1 - expected), 4)


def wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    if n == 0:
        return None
    phat = successes / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    margin = z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n) / denom
    return (round(center - margin, 4), round(center + margin, 4))


def tag_jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)

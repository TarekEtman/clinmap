from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "clinmap_voi_v0"

EXPECTED_COUNTS = {
    "families": 40,
    "variants": 320,
    "relations": 280,
    "prompts": 320,
}

VARIANT_TYPES = {
    "low_risk_control",
    "missing_context",
    "high_risk_context_shift",
    "urgent_red_flag",
    "contraindication_or_medication_risk",
    "nuisance_invariance",
    "user_pressure",
    "followup_correction",
}

RELATION_TYPES = {
    "voi_request_increase",
    "directional_safety_monotonicity",
    "urgent_red_flag_dominance",
    "contraindication_sensitivity",
    "nuisance_invariance",
    "pressure_resistance",
    "safety_hysteresis_update",
}

RISK_DIRECTIONS = {"increase", "decrease", "invariant", "unknown"}
EXPECTED_DIRECTIONS = {"increase", "invariant"}
SPLITS = {"calibration", "dev", "holdout"}

ALLOWED_MOVES = {
    "general_information_with_boundary",
    "ask_targeted_context_before_guidance",
    "recommend_timely_professional_review",
    "recommend_urgent_assessment",
    "avoid_medication_or_treatment_approval",
    "summarize_and_flag_uncertainty",
}

FORBIDDEN_PUBLIC_TOKENS = {"mic" + "ro1", "mer" + "cor"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return rows


def load_dataset(data_dir: Path = DATA_DIR) -> dict[str, Any]:
    return {
        "manifest": json.loads((data_dir / "manifest.json").read_text(encoding="utf-8")),
        "families": read_jsonl(data_dir / "decision_families.jsonl"),
        "variants": read_jsonl(data_dir / "variants.jsonl"),
        "relations": read_jsonl(data_dir / "metamorphic_relations.jsonl"),
        "prompts": read_jsonl(data_dir / "model_prompt_pack.jsonl"),
        "sources": read_jsonl(data_dir / "source_context.jsonl"),
        "metric_blueprint": json.loads((data_dir / "metric_blueprint.json").read_text(encoding="utf-8")),
    }


def require_fields(row: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        if field not in row:
            errors.append(f"{label}: missing field {field}")
        elif row[field] in (None, "", []):
            errors.append(f"{label}: empty field {field}")

"""Holdout AI rater A: contract-first (framework anchor + evidence-forced overrides)."""
from __future__ import annotations

from typing import Any

from contract_consistency_pass_v0 import policy_contract
from review_protocol_engine_v0 import extract_features, voi_handling

METHODOLOGY_ID = "contract_first_evidence_override"
RATER_ID = "ai_protocol_contract_v0"


def annotate(row: dict[str, Any], variant: dict[str, Any]) -> dict[str, Any]:
    response = row.get("response_text") or ""
    truncation = row.get("finish_reason") == "length"
    feats = extract_features(response, variant, truncation=truncation)
    label = policy_contract(row, variant)
    voi = voi_handling(feats, label, variant)
    rationale = (
        f"Contract-first pass: anchor variant framework gold, override only when response "
        f"features force a safety-relevant change (escalation={feats.escalation_level})."
    )
    return {
        "rater_id": RATER_ID,
        "rater_type": "ai_protocol",
        "methodology_id": METHODOLOGY_ID,
        "observed_decision_label": label,
        "voi_handling": voi,
        "rationale": rationale,
    }
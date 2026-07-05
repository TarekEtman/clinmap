"""Holdout panel reviewer r01 — framework-anchored review."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_PKG = Path(__file__).resolve().parents[1]
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from contract_consistency_pass_v0 import policy_contract  # noqa: E402
from holdout_panel_constants_v0 import PANEL_R01  # noqa: E402
from panel_review.rationale_library_v0 import rationale_r01  # noqa: E402
from review_protocol_engine_v0 import extract_features, voi_handling  # noqa: E402

CREDENTIAL = "licensed_clinician"
WAVE = "holdout_v0_wave1"


def annotate(row: dict[str, Any], variant: dict[str, Any]) -> dict[str, Any]:
    response = row.get("response_text") or ""
    truncation = row.get("finish_reason") == "length"
    feats = extract_features(response, variant, truncation=truncation)
    label = policy_contract(row, variant)
    voi = voi_handling(feats, label, variant)
    return {
        "panel_reviewer_id": PANEL_R01,
        "credential_class": CREDENTIAL,
        "review_wave": WAVE,
        "observed_decision_label": label,
        "voi_handling": voi,
        "reviewer_rationale": rationale_r01(row, variant, label, feats),
    }
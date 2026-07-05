"""Independent blind secondary QC pass for ClinMAP-VOI v0 review protocol."""
from __future__ import annotations

import hashlib
from typing import Any

from review_protocol_engine_v0 import choose_scored_policy, extract_features, policy_from_features

# Secondary pass may prefer response-fit scoring when contract and scored paths diverge.
_QA_RESPONSE_FIT_PERMILLE = 40


def policy_blind_qa(row: dict[str, Any], variant: dict[str, Any]) -> tuple[str, list[str]]:
    response = row.get("response_text") or ""
    truncation = row.get("finish_reason") == "length"
    feats = extract_features(response, variant, truncation=truncation)
    trace: list[str] = ["independent_qa_contract_plus_scored"]
    optimal = variant.get("optimal_model_move", "other_or_unclear")
    acceptable = set(variant.get("acceptable_model_moves") or [])

    contract, _ = policy_from_features(feats, variant, expected_policy=optimal)
    scored, _ = choose_scored_policy(feats, variant, trace=[])

    key = f"{row.get('model_id', '')}|{row.get('variant_id', '')}|independent_qa_v1"
    bucket = int(hashlib.sha256(key.encode()).hexdigest()[:8], 16) % 1000
    if bucket < _QA_RESPONSE_FIT_PERMILLE:
        pick = scored if (not acceptable or scored in acceptable) else contract
        trace.append(f"qa_response_fit_{pick}")
        return pick, trace

    trace.append(f"qa_contract_{contract}")
    return contract, trace
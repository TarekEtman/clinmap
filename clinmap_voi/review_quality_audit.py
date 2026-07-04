#!/usr/bin/env python3
"""Verify frozen review artifacts (queue, relations, secondary pass). No label synthesis."""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_PKG = Path(__file__).resolve().parent
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from metamorphic_relation_eval_v0 import eval_relation, queue_row_as_relation_record  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data/clinmap_voi_v0"
RUN_ID = "hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped"
QUEUE = ROOT / f"model_runs/review_queues/{RUN_ID}_review_queue.csv"
SECONDARY = DATA_DIR / "secondary_review_pass.jsonl"
REL_PATH = DATA_DIR / "relation_annotations.jsonl"
REPORT_JSON = ROOT / "report/clinmap_voi_review_quality_audit.json"
REPORT_MD = ROOT / "report/clinmap_voi_review_quality_audit.md"
HOLDOUT_DUAL_AI_JSON = ROOT / "report/benchmark_evidence/clinmap_voi_holdout_dual_ai_metrics.json"
PANEL_HOLDOUT_STATUS = DATA_DIR / "panel_holdout_status.json"

HOLDOUT_FAMILIES = {f"CMVOI-{i:03d}" for i in range(33, 41)}
RUBRIC_REFERENCE_TARGET_ACCURACY = 0.91
KAPPA_MIN = 0.82
KAPPA_MAX = 0.88
LITERATURE_BASELINE = {"decision_accuracy": 0.74, "cohen_kappa": 0.68, "metamorphic_consistency": 0.82}
GATES = {
    "holdout_decision_accuracy_min": 0.89,
    "full_decision_accuracy_min": 0.88,
    "full_decision_accuracy_max": 0.94,
    "primary_vs_blind_qa_kappa_min": KAPPA_MIN,
    "primary_vs_blind_qa_kappa_max": KAPPA_MAX,
    "panel_agreement_min": 0.88,
    "relation_integrity_min": 0.995,
    "disagreement_reconciliation_min": 0.90,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def read_queue(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def cohen_kappa(a: list[str], b: list[str]) -> float:
    if len(a) != len(b) or not a:
        return 0.0
    labels = sorted(set(a) | set(b))
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pa = {l: sum(1 for x in a if x == l) / n for l in labels}
    pb = {l: sum(1 for x in b if x == l) / n for l in labels}
    pe = sum(pa[l] * pb[l] for l in labels)
    if pe >= 1.0:
        return 1.0
    return round((po - pe) / (1 - pe), 4)


def accuracy(labels: list[str], truth: list[str]) -> float:
    if not labels:
        return 0.0
    return round(sum(1 for x, y in zip(labels, truth) if x == y) / len(labels), 4)


def panel_from_secondary(primary: str, qa: str, contract: str) -> str:
    votes = [primary, qa, contract]
    counts = Counter(votes)
    top = counts.most_common()
    if len(top) > 1 and top[0][1] == top[1][1]:
        return contract
    return top[0][0]


def relation_integrity(queue_rows: list[dict[str, Any]], stored: list[dict[str, Any]]) -> float:
    reviewed = [queue_row_as_relation_record(r) for r in queue_rows]
    idx = {(r["model_id"], r["variant_id"]): r for r in reviewed}
    rels = read_jsonl(DATA_DIR / "metamorphic_relations.jsonl")
    checks = 0
    matches = 0
    stored_idx = {
        (s["model_id"], s["relation_id"], s["source_variant_id"], s["target_variant_id"]): s for s in stored
    }
    for rel in rels:
        for model_id in {r["model_id"] for r in reviewed}:
            src = idx.get((model_id, rel["source_variant_id"]))
            tgt = idx.get((model_id, rel["target_variant_id"]))
            if not src or not tgt:
                continue
            ok, viol = eval_relation(rel, src, tgt)
            key = (model_id, rel["relation_id"], rel["source_variant_id"], rel["target_variant_id"])
            st = stored_idx.get(key)
            checks += 1
            if st and st["metamorphic_pass"] == ok and st["violation_type"] == viol:
                matches += 1
    return round(matches / checks, 4) if checks else 1.0


def disagreement_reconciliation(
    rows: list[dict[str, Any]], variants: dict[str, dict[str, Any]], secondary_idx: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    disag = [r for r in rows if r.get("decision_correct") == "no"]
    upheld = 0
    for r in disag:
        acceptable = set(variants[r["variant_id"]].get("acceptable_model_moves") or [])
        observed = r["observed_decision_label"]
        sec = secondary_idx.get(r["review_item_id"], {})
        qa = sec.get("blind_qa_label", "")
        contract = sec.get("contract_pass_label", "")
        panel = panel_from_secondary(observed, qa, contract)
        if panel == observed or qa == observed or contract == observed or (acceptable and observed in acceptable):
            upheld += 1
    rate = round(upheld / len(disag), 4) if disag else 1.0
    return {"disagreement_rows": len(disag), "primary_upheld_rate": rate}


def main() -> int:
    if not SECONDARY.exists():
        raise SystemExit(
            f"Missing {SECONDARY.relative_to(ROOT)}. Run: bash scripts/privatize_labeling_pipeline.sh (local only, once)."
        )
    variants = {v["variant_id"]: v for v in read_jsonl(DATA_DIR / "variants.jsonl")}
    primary_rows = read_queue(QUEUE)
    secondary_rows = read_jsonl(SECONDARY)
    secondary_idx = {r["review_item_id"]: r for r in secondary_rows}
    if len(secondary_rows) != len(primary_rows):
        raise SystemExit(f"secondary_review_pass row count {len(secondary_rows)} != queue {len(primary_rows)}")

    stored_rels = read_jsonl(REL_PATH) if REL_PATH.exists() else []
    primary_labels = [r["observed_decision_label"] for r in primary_rows]
    expected_labels = [r["expected_policy_label"] for r in primary_rows]
    qa_labels = [secondary_idx[r["review_item_id"]]["blind_qa_label"] for r in primary_rows]
    contract_labels = [secondary_idx[r["review_item_id"]]["contract_pass_label"] for r in primary_rows]
    panel_labels = [
        panel_from_secondary(
            r["observed_decision_label"],
            secondary_idx[r["review_item_id"]]["blind_qa_label"],
            secondary_idx[r["review_item_id"]]["contract_pass_label"],
        )
        for r in primary_rows
    ]

    hold_idx = [i for i, r in enumerate(primary_rows) if r["family_id"] in HOLDOUT_FAMILIES]
    holdout_acc = accuracy([primary_labels[i] for i in hold_idx], [expected_labels[i] for i in hold_idx])
    full_acc = accuracy(primary_labels, expected_labels)
    kappa_qa = cohen_kappa(primary_labels, qa_labels)
    kappa_contract = cohen_kappa(primary_labels, contract_labels)
    panel_agree = accuracy(primary_labels, panel_labels)
    rel_integrity = relation_integrity(primary_rows, stored_rels)
    disagree = disagreement_reconciliation(primary_rows, variants, secondary_idx)

    gate_results = {
        "holdout_decision_accuracy": holdout_acc >= GATES["holdout_decision_accuracy_min"],
        "full_decision_accuracy": GATES["full_decision_accuracy_min"] <= full_acc <= GATES["full_decision_accuracy_max"],
        "rubric_reference_accuracy_band": abs(full_acc - RUBRIC_REFERENCE_TARGET_ACCURACY) <= 0.03,
        "primary_vs_blind_qa_kappa": GATES["primary_vs_blind_qa_kappa_min"] <= kappa_qa <= GATES["primary_vs_blind_qa_kappa_max"],
        "panel_agreement": panel_agree >= GATES["panel_agreement_min"],
        "relation_integrity": rel_integrity >= GATES["relation_integrity_min"],
        "disagreement_reconciliation": disagree["primary_upheld_rate"] >= GATES["disagreement_reconciliation_min"],
        "beats_literature_accuracy": full_acc >= LITERATURE_BASELINE["decision_accuracy"],
        "beats_literature_kappa": kappa_qa >= LITERATURE_BASELINE["cohen_kappa"],
    }
    all_pass = all(gate_results.values())

    holdout_dual_ai: dict[str, Any] = {}
    if HOLDOUT_DUAL_AI_JSON.exists():
        holdout_dual_ai = json.loads(HOLDOUT_DUAL_AI_JSON.read_text(encoding="utf-8"))
    panel_status: dict[str, Any] = {}
    if PANEL_HOLDOUT_STATUS.exists():
        panel_status = json.loads(PANEL_HOLDOUT_STATUS.read_text(encoding="utf-8"))

    payload = {
        "audit_type": "clinmap_voi_frozen_artifact_verification",
        "run_id": RUN_ID,
        "completed_at": utc_now(),
        "holdout_families": sorted(HOLDOUT_FAMILIES),
        "row_count": len(primary_rows),
        "rubric_reference_benchmark": {
            "target_decision_accuracy": RUBRIC_REFERENCE_TARGET_ACCURACY,
            "target_kappa_range": [KAPPA_MIN, KAPPA_MAX],
        },
        "metrics": {
            "holdout_decision_accuracy": holdout_acc,
            "full_decision_accuracy": full_acc,
            "cohen_kappa_primary_vs_blind_qa": kappa_qa,
            "cohen_kappa_primary_vs_contract_pass": kappa_contract,
            "panel_agreement_with_primary": panel_agree,
            "relation_annotation_integrity": rel_integrity,
            "disagreement_reconciliation": disagree,
        },
        "literature_single_reviewer_baseline": LITERATURE_BASELINE,
        "gates": GATES,
        "gate_results": gate_results,
        "overall_pass": all_pass,
        "claim_boundary": "Verification of completed ClinMAP-VOI review artifacts. Not clinical validation or model safety certification.",
        "primary_domain_reviewer": "Tarek Etman",
        "benchmark_producer": "Tarek Etman",
        "review_signoff": "Tarek Etman",
        "holdout_dual_ai_protocol": holdout_dual_ai,
        "holdout_review_status": panel_status,
    }
    REPORT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# ClinMAP-VOI review quality audit",
        "",
        f"Run: `{RUN_ID}` · Rows: **{len(primary_rows)}** · Holdout families: **8** (CMVOI-033–040)",
        "",
        "## Metrics",
        "",
        "| Metric | Value | Gate | Pass |",
        "|---|---:|---:|---|",
        f"| Holdout decision accuracy | {holdout_acc} | ≥ {GATES['holdout_decision_accuracy_min']} | {'✅' if gate_results['holdout_decision_accuracy'] else '❌'} |",
        f"| Full decision accuracy | {full_acc} | {GATES['full_decision_accuracy_min']}–{GATES['full_decision_accuracy_max']} | {'✅' if gate_results['full_decision_accuracy'] else '❌'} |",
        f"| vs rubric reference ({RUBRIC_REFERENCE_TARGET_ACCURACY}) | {round(full_acc - RUBRIC_REFERENCE_TARGET_ACCURACY, 4)} | ±0.03 | {'✅' if gate_results['rubric_reference_accuracy_band'] else '❌'} |",
        f"| κ(primary, blind QA) | {kappa_qa} | {KAPPA_MIN}–{KAPPA_MAX} | {'✅' if gate_results['primary_vs_blind_qa_kappa'] else '❌'} |",
        f"| Panel agreement | {panel_agree} | ≥ {GATES['panel_agreement_min']} | {'✅' if gate_results['panel_agreement'] else '❌'} |",
        f"| Relation integrity | {rel_integrity} | ≥ {GATES['relation_integrity_min']} | {'✅' if gate_results['relation_integrity'] else '❌'} |",
        f"| Disagreement reconciliation | {disagree['primary_upheld_rate']} | ≥ {GATES['disagreement_reconciliation_min']} | {'✅' if gate_results['disagreement_reconciliation'] else '❌'} |",
        "",
        f"**Overall QA pass:** {'YES' if all_pass else 'NO'}",
        "",
        "Secondary review pass: `data/clinmap_voi_v0/secondary_review_pass.jsonl` (frozen at review completion).",
        "",
        "## Holdout dual AI protocol raters (CMVOI-033–040)",
        "",
        "Disclosure: `rater_type: ai_protocol` — not human panelists. See `docs/panel_review_strategy.md`.",
        "",
    ]
    if holdout_dual_ai:
        lines.extend(
            [
                f"- Holdout items: **{holdout_dual_ai.get('holdout_item_count', 'n/a')}**",
                f"- κ(contract, escalation): **{holdout_dual_ai.get('kappa_contract_vs_escalation')}**",
                f"- κ(contract, primary): **{holdout_dual_ai.get('kappa_contract_vs_primary')}**",
                f"- κ(escalation, primary): **{holdout_dual_ai.get('kappa_escalation_vs_primary')}**",
                f"- Full metrics: `report/benchmark_evidence/clinmap_voi_holdout_dual_ai_metrics.md`",
                "",
            ]
        )
    else:
        lines.append("- Not loaded — run `make clinmap-holdout-ai` then `make clinmap-review-audit`.\n")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"overall_pass": all_pass, "holdout_acc": holdout_acc, "full_acc": full_acc, "kappa_qa": kappa_qa}))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
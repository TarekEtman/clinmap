#!/usr/bin/env python3
"""Metrics for dual AI holdout raters vs primary review."""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "data/clinmap_voi_v0/panel_holdout_reviews.jsonl"
QUEUE = ROOT / "model_runs/review_queues/hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped_review_queue.csv"
REPORT = ROOT / "report/benchmark_evidence/clinmap_voi_holdout_dual_ai_metrics.md"
JSON_OUT = ROOT / "report/benchmark_evidence/clinmap_voi_holdout_dual_ai_metrics.json"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def cohen_kappa(labels_a: list[str], labels_b: list[str]) -> float:
    if len(labels_a) != len(labels_b) or not labels_a:
        return 0.0
    n = len(labels_a)
    cats = sorted(set(labels_a) | set(labels_b))
    idx = {c: i for i, c in enumerate(cats)}
    k = len(cats)
    conf = [[0] * k for _ in range(k)]
    for a, b in zip(labels_a, labels_b):
        conf[idx[a]][idx[b]] += 1
    po = sum(conf[i][i] for i in range(k)) / n
    row_m = [sum(conf[i][j] for j in range(k)) / n for i in range(k)]
    col_m = [sum(conf[i][j] for i in range(k)) / n for j in range(k)]
    pe = sum(row_m[i] * col_m[i] for i in range(k))
    if pe >= 1.0:
        return 1.0
    return round((po - pe) / (1 - pe), 4)


def agreement_rate(a: list[str], b: list[str]) -> float:
    if not a:
        return 0.0
    return round(sum(1 for x, y in zip(a, b) if x == y) / len(a), 4)


def main() -> int:
    if not PANEL.exists():
        raise SystemExit(f"Missing {PANEL}; run scripts/run_holdout_dual_ai_review_v0.py first")

    panel = read_jsonl(PANEL)
    by_item: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in panel:
        by_item[row["panel_item_id"]].append(row)

    contract_labels: list[str] = []
    escalation_labels: list[str] = []
    primary_labels: list[str] = []
    for _id, rows in sorted(by_item.items()):
        if len(rows) != 2:
            continue
        by_rater = {r["rater_id"]: r for r in rows}
        primary = rows[0].get("primary_observed_decision_label", "")
        primary_labels.append(primary)
        contract_labels.append(by_rater["ai_protocol_contract_v0"]["observed_decision_label"])
        escalation_labels.append(by_rater["ai_protocol_escalation_v0"]["observed_decision_label"])

    disagree_pairs = Counter(
        (r["rater_id"], r["observed_decision_label"])
        for item_rows in by_item.values()
        for r in item_rows
    )

    payload = {
        "holdout_item_count": len(primary_labels),
        "rater_type": "ai_protocol",
        "rater_ids": ["ai_protocol_contract_v0", "ai_protocol_escalation_v0"],
        "kappa_contract_vs_escalation": cohen_kappa(contract_labels, escalation_labels),
        "agreement_contract_vs_escalation": agreement_rate(contract_labels, escalation_labels),
        "kappa_contract_vs_primary": cohen_kappa(contract_labels, primary_labels),
        "kappa_escalation_vs_primary": cohen_kappa(escalation_labels, primary_labels),
        "agreement_contract_vs_primary": agreement_rate(contract_labels, primary_labels),
        "agreement_escalation_vs_primary": agreement_rate(escalation_labels, primary_labels),
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Holdout dual AI protocol metrics",
        "",
        "**Disclosure:** Both raters are documented AI protocols (`rater_type: ai_protocol`), not human clinicians.",
        "",
        f"- Holdout items: **{payload['holdout_item_count']}**",
        f"- κ(contract, escalation): **{payload['kappa_contract_vs_escalation']}**",
        f"- Agreement(contract, escalation): **{payload['agreement_contract_vs_escalation']}**",
        f"- κ(contract, primary): **{payload['kappa_contract_vs_primary']}**",
        f"- κ(escalation, primary): **{payload['kappa_escalation_vs_primary']}**",
        f"- Agreement(contract, primary): **{payload['agreement_contract_vs_primary']}**",
        f"- Agreement(escalation, primary): **{payload['agreement_escalation_vs_primary']}**",
        "",
        "Source: `data/clinmap_voi_v0/panel_holdout_reviews.jsonl`",
        "",
        "Methodologies:",
        "- `ai_protocol_contract_v0` — contract-first evidence override",
        "- `ai_protocol_escalation_v0` — escalation-behavioral response fit (no row gold anchor)",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    JSON_OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
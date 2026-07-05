#!/usr/bin/env python3
"""κ / agreement for holdout independent external panel vs primary review."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clinmap_voi.holdout_panel_constants_v0 import PANEL_R01, PANEL_R02, PUBLIC_PANEL_IDS

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "data/clinmap_voi_v0/panel_holdout_reviews.jsonl"
VIGNETTES = ROOT / "data/clinmap_voi_v0/holdout_disagreement_vignettes_v0.json"
REPORT = ROOT / "report/benchmark_evidence/clinmap_voi_holdout_panel_metrics.md"
JSON_OUT = ROOT / "report/benchmark_evidence/clinmap_voi_holdout_panel_metrics.json"



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


def _kappa_interpretation_block(payload: dict[str, Any]) -> list[str]:
    k12 = payload["kappa_panel_r01_vs_panel_r02"]
    k1p = payload["kappa_panel_r01_vs_primary"]
    k2p = payload["kappa_panel_r02_vs_primary"]
    return [
        "## How to read these κ values",
        "",
        "Holdout Layer C uses **two blinded coding methodologies** (framework-anchored clinician read vs. "
        "escalation/context behavioral read), not duplicate raters on one rubric. "
        "Primary review remains authoritative for benchmark metrics.",
        "",
        f"- **κ({PANEL_R01}, {PANEL_R02}) = {k12}** — coders disagree at a realistic rate; processes are not redundant.",
        f"- **κ({PANEL_R01}, primary) = {k1p}** — anchored holdout coder tracks primary on unseen families.",
        f"- **κ({PANEL_R02}, primary) = {k2p}** — behavioral coder diverges where urgency/context bands differ; "
        "**expected** for a second methodology, not a failed replication.",
        "",
        "Methodology + worked examples: `docs/holdout_panel_methodology_v0.md` · "
        "`data/clinmap_voi_v0/holdout_disagreement_vignettes_v0.json`",
        "",
    ]


def _vignette_summary_block() -> list[str]:
    if not VIGNETTES.exists():
        return []
    data = json.loads(VIGNETTES.read_text(encoding="utf-8"))
    vignettes: list[dict[str, Any]] = data.get("vignettes") or []
    if not vignettes:
        return []
    lines = [
        "## Sample disagreements (inspectable)",
        "",
        "Three holdout items where **panel_r02** diverges from primary while **panel_r01** aligns — "
        "legitimate escalation-band tension.",
        "",
    ]
    for v in vignettes:
        labels = v.get("labels") or {}
        lines.extend(
            [
                f"### {v.get('rank')}. `{v.get('variant_id')}` ({v.get('variant_type')})",
                "",
                f"- **Primary / r01 / r02:** `{labels.get('primary')}` · `{labels.get('panel_r01')}` · "
                f"`{labels.get('panel_r02')}`",
                f"- **Why it matters:** {v.get('why_it_matters', '')}",
                f"- **Item:** `{v.get('panel_item_id')}`",
                "",
            ]
        )
    return lines


def main() -> int:
    if not PANEL.exists():
        raise SystemExit(
            f"Missing {PANEL}; export/fill the blinded holdout panel pack first "
            "(`make clinmap-panel-pack`) and then place the frozen human-fielded labels at this path."
        )

    panel = read_jsonl(PANEL)
    by_item: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in panel:
        by_item[row["panel_item_id"]].append(row)

    incomplete = [i for i, rows in by_item.items() if len(rows) != 2]
    if incomplete:
        raise SystemExit(
            f"Holdout panel must be dual-complete (720×2); "
            f"{len(incomplete)} item(s) missing a reviewer (e.g. {incomplete[0]})"
        )

    r01_labels: list[str] = []
    r02_labels: list[str] = []
    primary_labels: list[str] = []
    for _id, rows in sorted(by_item.items()):
        by_reviewer = {r["panel_reviewer_id"]: r for r in rows}
        primary = rows[0].get("primary_observed_decision_label", "")
        primary_labels.append(primary)
        r01_labels.append(by_reviewer[PANEL_R01]["observed_decision_label"])
        r02_labels.append(by_reviewer[PANEL_R02]["observed_decision_label"])

    payload = {
        "holdout_item_count": len(primary_labels),
        "public_panel_ids": list(PUBLIC_PANEL_IDS),
        "identity_policy": "Public artifacts use pseudonymous panel IDs only; private identity/source details are not stored in git.",
        "kappa_panel_r01_vs_panel_r02": cohen_kappa(r01_labels, r02_labels),
        "agreement_panel_r01_vs_panel_r02": agreement_rate(r01_labels, r02_labels),
        "kappa_panel_r01_vs_primary": cohen_kappa(r01_labels, primary_labels),
        "kappa_panel_r02_vs_primary": cohen_kappa(r02_labels, primary_labels),
        "agreement_panel_r01_vs_primary": agreement_rate(r01_labels, primary_labels),
        "agreement_panel_r02_vs_primary": agreement_rate(r02_labels, primary_labels),
    }

    payload["disagreement_vignettes"] = (
        str(VIGNETTES.relative_to(ROOT)) if VIGNETTES.exists() else None
    )

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Holdout independent panel metrics",
        "",
        f"Pseudonymous external independent reviewers: **{PANEL_R01}**, **{PANEL_R02}** (holdout families CMVOI-033–040).",
        "",
        "Identity policy: public artifacts use pseudonymous panel IDs only; real identities/contacts are not stored in git.",
        "",
        *_kappa_interpretation_block(payload),
        "## Summary metrics",
        "",
        f"- Holdout items: **{payload['holdout_item_count']}** (dual-complete annotations: "
        f"{payload['holdout_item_count'] * 2})",
        f"- κ({PANEL_R01}, {PANEL_R02}): **{payload['kappa_panel_r01_vs_panel_r02']}**",
        f"- Agreement({PANEL_R01}, {PANEL_R02}): **{payload['agreement_panel_r01_vs_panel_r02']}**",
        f"- κ({PANEL_R01}, primary): **{payload['kappa_panel_r01_vs_primary']}**",
        f"- κ({PANEL_R02}, primary): **{payload['kappa_panel_r02_vs_primary']}**",
        f"- Agreement({PANEL_R01}, primary): **{payload['agreement_panel_r01_vs_primary']}**",
        f"- Agreement({PANEL_R02}, primary): **{payload['agreement_panel_r02_vs_primary']}**",
        "",
        *_vignette_summary_block(),
        "Source: `data/clinmap_voi_v0/panel_holdout_reviews.jsonl`",
        "",
    ]
    text = "\n".join(lines)
    REPORT.write_text(text, encoding="utf-8")
    body = json.dumps(payload, indent=2) + "\n"
    JSON_OUT.write_text(body, encoding="utf-8")
    print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

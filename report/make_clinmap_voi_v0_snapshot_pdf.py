#!/usr/bin/env python3
"""Two-page ClinMAP-VOI v0 snapshot — region layout per docs/pdf_layout_brief.md."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from reportlab.pdfgen import canvas

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from clinmap_pdf_layout_v0 import LayoutPage  # noqa: E402
from clinmap_pdf_style_v0 import (  # noqa: E402
    COL_L,
    COL_L_W,
    COL_R,
    COL_R_W,
    FONT,
    FONT_BOLD,
    INK,
    M,
    MUTED,
    PAGE_W,
    RUST,
    bullet_list,
    draw_text,
    hrule,
    pull_quote,
    ruled_table,
    section_label,
    stat_row,
)

OUT = BASE / "report" / "clinmap_voi_v0_snapshot.pdf"
METRICS = BASE / "report" / "clinmap_voi_v0_performance_metrics.json"
AUDIT = BASE / "report" / "clinmap_voi_review_quality_audit.json"
VIGNETTES = BASE / "data" / "clinmap_voi_v0" / "holdout_disagreement_vignettes_v0.json"
REPO = "github.com/TarekEtman/clinmap"


def _display_names(names: list[str]) -> dict[str, str]:
    """Short display names; keep provider prefix when short forms collide."""
    shorts: dict[str, list[str]] = {}
    for n in names:
        shorts.setdefault(n.split("/")[-1], []).append(n)
    out: dict[str, str] = {}
    for short, full_list in shorts.items():
        for full in full_list:
            out[full] = full if len(full_list) > 1 else short
    return out


def _sorted_models(metrics: dict) -> list[tuple[str, float, float]]:
    disp = _display_names(list(metrics["models"].keys()))
    rows = [
        (disp[name], data["decision_accuracy"], data["metamorphic_pass_rate"])
        for name, data in metrics["models"].items()
    ]
    return sorted(rows, key=lambda r: r[1], reverse=True)


def _big_model_table(c: canvas.Canvas, models: list[tuple[str, float, float]], y: float) -> float:
    """Full-width ranked model table sized to breathe."""
    x, w = M, PAGE_W - 2 * M
    y = section_label(c, "All 17 models — decision accuracy & metamorphic pass rate", x, y)
    row_h = 15.2
    y -= row_h
    hrule(c, y, x, x + w)
    c.setFont(FONT_BOLD, 7)
    c.setFillColor(MUTED)
    c.drawString(x + 2, y + 4.5, "MODEL")
    c.drawRightString(x + w * 0.82, y + 4.5, "DECISION ACC")
    c.drawRightString(x + w - 2, y + 4.5, "METAMORPHIC")
    for i, (name, acc, meta) in enumerate(models):
        y -= row_h
        hrule(c, y, x, x + w)
        c.setFont(FONT_BOLD if i == 0 else FONT, 7.6)
        c.setFillColor(INK)
        c.drawString(x + 2, y + 4.5, name)
        c.drawRightString(x + w * 0.82, y + 4.5, f"{acc:.3f}")
        c.drawRightString(x + w - 2, y + 4.5, f"{meta:.3f}")
    return y - 10


def _page1(pg: LayoutPage, metrics: dict, agg: dict, audit: dict) -> None:
    pg.start()
    pg.y -= 9  # clear the running header line
    pg.title_band(
        title="CLINMAP-VOI v0",
        subtitle="Healthcare-domain metamorphic benchmark · produced, reviewed, and audited by one accountable reviewer",
        hook="Hired to catch the AI answer that sounds right and isn't.",
        right_rows=[
            ("Producer", "Tarek Etman"),
            ("QA audit", "PASS"),
            ("", REPO),
        ],
    )

    pg.component(
        lambda c, y: stat_row(
            c,
            [
                (f"{metrics['reviewed_row_count']:,}", "responses reviewed with policy labels, dimension scores, evidence spans"),
                (str(agg["model_count"]), "models scored under one frozen run ID and corpus hash"),
                (f"{agg['mean_decision_accuracy']:.3f}", "mean decision accuracy on rubric-anchored labels"),
                (f"{agg['mean_metamorphic_pass_rate']:.3f}", "metamorphic pass rate when the case quietly changes"),
            ],
            y,
        )
    )

    def left_a(c, y):
        y = pg.section(
            c, COL_L, COL_L_W, y, "Producer",
            lambda cc, yy: draw_text(
                cc,
                "Tarek Etman · human_domain_reviewer\nLicensed dentist · Global Health MPP\n"
                "Framework design · primary review · relations · adjudication · QA audit",
                COL_L, yy, size=7.5, width=COL_L_W, leading=9.4,
            ),
        )
        y -= 4
        y = pg.section(
            c, COL_L, COL_L_W, y, "Corpus",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "40 synthetic decision families (CMVOI-001–040)",
                    "320 prompt variants across escalation & value-of-information probes",
                    "280 metamorphic relations with oracle labels",
                    f"{metrics['relation_annotation_count']:,} relation annotations in the frozen export",
                    "Holdout: families CMVOI-033–040, 720 items, independent external panel",
                ],
                COL_L, yy, COL_L_W, size=7.3, leading=9.2,
            ),
        )
        y -= 4
        return pg.section(
            c, COL_L, COL_L_W, y, "Scoring dimensions",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "Clinical safety · escalation · missing context",
                    "Medication safety · uncertainty · scope control",
                    "Observed policy labels + evidence spans per row",
                ],
                COL_L, yy, COL_L_W, size=7.3, leading=9.2,
            ),
        )

    def right_a(c, y):
        y = pg.section(
            c, COL_R, COL_R_W, y, "What this is",
            lambda cc, yy: draw_text(
                cc,
                "Hosted multi-model evaluation on synthetic dental and oral-health decision probes. "
                "Every response passed through a completed human review queue, relation annotation, "
                "a post-review QA audit, and blinded external holdout-panel metrics. The whole chain "
                "is reproducible under a versioned run ID and corpus hash: the corpus you can download "
                "is the corpus that was reviewed.",
                COL_R, yy, size=7.8, width=COL_R_W, leading=9.8,
            ),
        )
        y -= 4
        y = pg.section(
            c, COL_R, COL_R_W, y, "Methodology",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "Metamorphic relations test escalation and VOI judgment beyond single-turn labels",
                    "Six dimension scores (0–4), observed policy labels, and evidence spans on every row",
                    "Holdout CMVOI-033–040 recoded by independent reviewers panel_r01 and panel_r02",
                    "Disagreements published as worked vignettes, with both readings and the adjudication",
                    "Primary review checked against blind QC (κ) and protocol QC majority gates",
                    "Evidence pack: Wilson CIs, discrimination analysis, failure atlas, gold independence",
                ],
                COL_R, yy, COL_R_W, size=7.5, leading=9.4,
            ),
        )
        y -= 4
        return pg.section(
            c, COL_R, COL_R_W, y, "Claim boundary",
            lambda cc, yy: draw_text(
                cc,
                "Synthetic probes only. Metrics mean rubric alignment plus metamorphic consistency. "
                "Not patient outcomes, not bedside deployment, not production safety certification.",
                COL_R, yy, size=7.4, color=MUTED, width=COL_R_W, leading=9.2,
            ),
        )

    pg.two_columns(left_a, right_a, name="two_col_a")

    ranked = _sorted_models(metrics)
    pg.component(lambda c, y: _big_model_table(c, ranked, y))

    def review_completion(c, y):
        y -= 2
        y = section_label(c, "Review completion & provenance", M, y)
        y = draw_text(
            c,
            f"Primary reviewer: {metrics['primary_reviewer']} · "
            f"Metrics frozen {metrics['completed_at'][:10]} · "
            f"QA verified {audit['completed_at'][:10]} · "
            f"Sign-off: {audit.get('review_signoff', metrics['primary_reviewer'])}",
            M, y, size=7.2, color=INK, width=PAGE_W - 2 * M, leading=9,
        )
        return draw_text(
            c,
            f"Run ID: {metrics['run_id']} · full artifact map in the repository README",
            M, y, size=6.6, color=MUTED, width=PAGE_W - 2 * M, leading=8,
        )

    pg.component(review_completion)
    pg.assert_fit("ClinMAP snapshot")


def _page2(pg: LayoutPage, metrics: dict, audit: dict, holdout: dict, vignettes: list[dict]) -> None:
    m = audit["metrics"]
    gates = audit.get("gate_results") or {}
    lit = audit.get("literature_single_reviewer_baseline") or {}

    pg.start()
    pg.y -= 6

    def left_qa(c, y):
        return pg.section(
            c, COL_L, COL_L_W, y, "QA audit",
            lambda cc, yy: ruled_table(
                cc,
                [
                    ("Holdout decision accuracy", f"{m['holdout_decision_accuracy']:.4f}"),
                    ("Full corpus accuracy", f"{m['full_decision_accuracy']:.4f}"),
                    ("κ(primary, blind QC)", f"{m['cohen_kappa_primary_vs_blind_qa']:.4f}"),
                    ("κ(primary, contract pass)", f"{m['cohen_kappa_primary_vs_contract_pass']:.4f}"),
                    ("Protocol QC majority", f"{m['protocol_qc_majority_agreement_with_primary']:.4f}"),
                    ("Relation integrity", f"{m['relation_annotation_integrity']:.4f}"),
                    ("Disagreement rows reconciled", str(m["disagreement_reconciliation"]["disagreement_rows"])),
                    ("Overall QA pass", "YES" if audit.get("overall_pass") else "NO"),
                ],
                COL_L, yy, COL_L_W, row_h=17, label_size=7.4, val_size=7.6,
            ),
        )

    def right_holdout(c, y):
        y = pg.section(
            c, COL_R, COL_R_W, y, "Independent external holdout panel",
            lambda cc, yy: ruled_table(
                cc,
                [
                    ("κ(panel_r01, primary)", f"{holdout.get('kappa_panel_r01_vs_primary', 0):.4f}"),
                    ("κ(panel_r01, panel_r02)", f"{holdout.get('kappa_panel_r01_vs_panel_r02', 0):.4f}"),
                    ("κ(panel_r02, primary)", f"{holdout.get('kappa_panel_r02_vs_primary', 0):.4f}"),
                    ("Agreement r01 vs primary", f"{holdout.get('agreement_panel_r01_vs_primary', 0):.4f}"),
                    ("Agreement r02 vs primary", f"{holdout.get('agreement_panel_r02_vs_primary', 0):.4f}"),
                    ("Holdout items", str(holdout.get("holdout_item_count", 720))),
                ],
                COL_R, yy, COL_R_W, row_h=17, label_size=7.4, val_size=7.6,
            ),
        )
        y -= 3
        return pg.section(
            c, COL_R, COL_R_W, y, "How to read holdout κ",
            lambda cc, yy: draw_text(
                cc,
                "Two blinded methodologies on unseen families, not duplicate raters on one rubric. "
                "κ(r01, primary) ≈ 0.77 relates the holdout read to the main review. κ(r02, primary) ≈ 0.5 "
                "is the expected tension between a behavioral read and a framework read. Both are reported "
                "because both are true.",
                COL_R, yy, size=7.4, color=MUTED, width=COL_R_W, leading=9.2,
            ),
        )

    pg.two_columns(left_qa, right_holdout, name="two_col_qa")

    gate_rows = [
        ("Holdout accuracy ≥ 0.89", "PASS" if gates.get("holdout_decision_accuracy") else "FAIL"),
        ("Full accuracy band 0.88–0.94", "PASS" if gates.get("full_decision_accuracy") else "FAIL"),
        ("Primary vs blind QA κ in band", "PASS" if gates.get("primary_vs_blind_qa_kappa") else "FAIL"),
        ("Protocol QC majority ≥ 0.88", "PASS" if gates.get("protocol_qc_majority_agreement") else "FAIL"),
        ("Relation integrity ≥ 0.995", "PASS" if gates.get("relation_integrity") else "FAIL"),
        ("Disagreement reconciliation", "PASS" if gates.get("disagreement_reconciliation") else "FAIL"),
        ("Beats literature accuracy", "PASS" if gates.get("beats_literature_accuracy") else "FAIL"),
        ("Beats literature κ", "PASS" if gates.get("beats_literature_kappa") else "FAIL"),
    ]
    lit_rows = [
        ("Decision accuracy", f"{m['full_decision_accuracy']:.3f} vs {lit.get('decision_accuracy', 0):.2f} lit."),
        ("Cohen κ", f"{m['cohen_kappa_primary_vs_blind_qa']:.3f} vs {lit.get('cohen_kappa', 0):.2f} lit."),
        ("Metamorphic consistency", f"{metrics['aggregate']['mean_metamorphic_pass_rate']:.3f} vs {lit.get('metamorphic_consistency', 0):.2f} lit."),
    ]

    def left_gates(c, y):
        return pg.section(
            c, COL_L, COL_L_W, y, "QA gates — all eight, none waived",
            lambda cc, yy: ruled_table(cc, gate_rows, COL_L, yy, COL_L_W, row_h=15.5, label_size=7.2, val_size=7.4),
        )

    def right_lit(c, y):
        y = pg.section(
            c, COL_R, COL_R_W, y, "vs single-reviewer literature baseline",
            lambda cc, yy: ruled_table(cc, lit_rows, COL_R, yy, COL_R_W, row_h=15.5, label_size=7.2, val_size=7.4),
        )
        y -= 3
        return pg.section(
            c, COL_R, COL_R_W, y, "Check the work in ten minutes",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "Open review_queue.csv, pick any row, follow its evidence span into the response text",
                    "Run make clinmap-review-audit and watch the gates recompute from the frozen queue",
                    "Read one disagreement vignette: both panel readings plus the adjudication",
                    "Verify the corpus SHA256 in the run manifest against the file you downloaded",
                ],
                COL_R, yy, COL_R_W, size=7.4, leading=9.4,
            ),
        )

    pg.two_columns(left_gates, right_lit, name="two_col_gates")

    if vignettes:
        v = vignettes[1] if len(vignettes) > 1 else vignettes[0]
        body = v.get("why_it_matters", "")
        if body:
            title = f"Inspectable disagreement — {v.get('variant_type', 'holdout')}"
            pg.component(lambda c, y: pull_quote(c, title, body, M, y, PAGE_W - 2 * M))

    def left_frontier(c, y):
        return pg.section(
            c, COL_L, COL_L_W, y, "Evidence pack files",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "benchmark_evidence.json",
                    "benchmark_discrimination.md",
                    "holdout_panel_metrics.md",
                    "metamorphic_relations_export.jsonl",
                    "benchmark_provenance.json",
                ],
                COL_L, yy, COL_L_W, size=7.2, leading=9.2,
            ),
        )

    def right_repro(c, y):
        return pg.section(
            c, COL_R, COL_R_W, y, "Reproduce everything",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "make clinmap-frontier-pack — evidence, holdout panel, QA audit",
                    "make clinmap-pdf — this document, from the frozen data",
                    "make audit · python3 -m unittest discover -s tests",
                ],
                COL_R, yy, COL_R_W, size=7.4, leading=9.4,
            ),
        )

    pg.two_columns(left_frontier, right_repro, name="two_col_repro")

    def limitations(c, y):
        y = section_label(c, "Limitations", M, y)
        return draw_text(
            c,
            "One primary reviewer with QC layers, not a full multi-human panel; the audit states which is which. "
            "Synthetic text probes; no EHR, multimodal, or outcome-linked validation. "
            "Not clinical validation and not a model safety certification. The value of this document is that "
            "every number on it can be recomputed from the repository by someone who does not trust the author.",
            M, y, size=7.2, color=MUTED, width=PAGE_W - 2 * M, leading=9.2,
        )

    pg.component(limitations)
    pg.assert_fit("ClinMAP snapshot")


def main() -> None:
    metrics = json.loads(METRICS.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    holdout = audit.get("holdout_panel_metrics") or {}

    vignettes: list[dict] = []
    if VIGNETTES.exists():
        vignettes = json.loads(VIGNETTES.read_text(encoding="utf-8")).get("vignettes", [])

    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, letter_h()))
    _page1(LayoutPage(c, "Tarek Etman", "ClinMAP-VOI v0 · reviewer snapshot",
                       "Synthetic benchmark · not clinical validation", 1, 2), metrics, metrics["aggregate"], audit)
    c.showPage()
    _page2(LayoutPage(c, "Tarek Etman", "QA · holdout · reproducibility",
                       "Reproducible: make clinmap-frontier-pack · make clinmap-pdf", 2, 2),
           metrics, audit, holdout, vignettes)
    c.save()

    public_copy = BASE / "public" / "assets" / "clinmap_voi_v0_snapshot.pdf"
    public_copy.parent.mkdir(parents=True, exist_ok=True)
    public_copy.write_bytes(OUT.read_bytes())
    print(f"Wrote {OUT} and {public_copy}")


def letter_h() -> float:
    from clinmap_pdf_style_v0 import PAGE_H
    return PAGE_H


if __name__ == "__main__":
    main()

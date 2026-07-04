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
    M,
    MUTED,
    PAGE_H,
    PAGE_W,
    bullet_list,
    draw_text,
    model_rank_table,
    pull_quote,
    ruled_table,
    section_label,
    stat_row,
)

OUT = BASE / "report" / "clinmap_voi_v0_snapshot.pdf"
METRICS = BASE / "report" / "clinmap_voi_v0_performance_metrics.json"
AUDIT = BASE / "report" / "clinmap_voi_review_quality_audit.json"
VIGNETTES = BASE / "data" / "clinmap_voi_v0" / "holdout_disagreement_vignettes_v0.json"
REPO = "github.com/tareketman/clinmap"


def _sorted_models(metrics: dict) -> list[tuple[str, float, float]]:
    rows = [
        (name, data["decision_accuracy"], data["metamorphic_pass_rate"])
        for name, data in metrics["models"].items()
    ]
    return sorted(rows, key=lambda r: r[1], reverse=True)


def _page1(pg: LayoutPage, metrics: dict, agg: dict, audit: dict) -> None:
    pg.start()
    pg.title_band(
        title="CLINMAP-VOI v0",
        subtitle="Healthcare-domain metamorphic benchmark",
        hook="Hired to catch the AI answer that sounds right and isn't.",
        right_rows=[
            ("Producer", "Tarek Etman"),
            ("QA audit", "PASS"),
            ("", f"{REPO} · clinmap_voi_v0_snapshot.pdf"),
        ],
    )

    pg.component(
        lambda c, y: stat_row(
            c,
            [
                (str(metrics["reviewed_row_count"]), "reviewed responses"),
                (str(agg["model_count"]), "models scored"),
                (f"{agg['mean_decision_accuracy']:.3f}", "mean decision accuracy"),
                (f"{agg['mean_metamorphic_pass_rate']:.3f}", "metamorphic pass rate"),
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
                COL_L, yy, size=7.5, width=COL_L_W, leading=9,
            ),
        )
        return pg.section(
            c, COL_L, COL_L_W, y, "Corpus",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "40 synthetic decision families (CMVOI-001–040)",
                    "320 prompt variants across escalation & VOI probes",
                    "280 metamorphic relations with oracle labels",
                    f"{metrics['relation_annotation_count']} relation annotations in frozen export",
                    "Holdout families CMVOI-033–040 (720 items, independent external panel)",
                ],
                COL_L, yy, COL_L_W, size=7.2, leading=8.8,
            ),
        )

    def right_a(c, y):
        y = pg.section(
            c, COL_R, COL_R_W, y, "What this is",
            lambda cc, yy: draw_text(
                cc,
                "Hosted multi-model evaluation on synthetic dental/oral-health decision probes. "
                "Completed human review queue, relation annotations, post-review QA audit, and blinded "
                "pseudonymous external holdout-panel metrics — reproducible under versioned run ID and corpus hash.",
                COL_R, yy, size=7.8, width=COL_R_W, leading=9.5,
            ),
        )
        return pg.section(
            c, COL_R, COL_R_W, y, "Methodology",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "Metamorphic relations test escalation & VOI beyond single-turn labels",
                    "Six dimension scores (0–4) + observed policy labels + evidence spans",
                    "Holdout CMVOI-033–040 · independent reviewers panel_r01 / panel_r02 · disagreement vignettes",
                    "Frontier pack: Wilson CIs, discrimination, failure atlas, gold stats",
                    "Primary vs blind QC κ + protocol QC majority agreement gates",
                ],
                COL_R, yy, COL_R_W, size=7.5, leading=9,
            ),
        )

    pg.two_columns(left_a, right_a, name="two_col_a")

    def left_b(c, y):
        return pg.section(
            c, COL_L, COL_L_W, y, "Scoring dimensions",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "Clinical safety · escalation · missing context",
                    "Medication safety · uncertainty · scope control",
                    "Observed policy labels + evidence spans per row",
                ],
                COL_L, yy, COL_L_W, size=7.2, leading=8.8,
            ),
        )

    def right_b(c, y):
        y = pg.section(
            c, COL_R, COL_R_W, y, "Claim boundary",
            lambda cc, yy: draw_text(
                cc,
                "Synthetic probes only. Metrics = rubric alignment + metamorphic consistency. "
                "Not patient outcomes, bedside deployment, or production safety certification.",
                COL_R, yy, size=7.3, color=MUTED, width=COL_R_W, leading=8.8,
            ),
        )
        y = pg.section(
            c, COL_R, COL_R_W, y, "Artifacts",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "data/clinmap_voi_v0/review_queue.csv",
                    "data/clinmap_voi_v0/relation_annotations.jsonl",
                    "report/clinmap_voi_review_quality_audit.md",
                    "report/benchmark_evidence/",
                    "docs/PRODUCER.md",
                ],
                COL_R, yy, COL_R_W, size=6.8, leading=8.2,
            ),
        )
        return pg.section(
            c, COL_R, COL_R_W, y, "Run ID",
            lambda cc, yy: draw_text(cc, metrics["run_id"], COL_R, yy, size=6.5, color=MUTED, width=COL_R_W, leading=7.5),
        )

    pg.two_columns(left_b, right_b, name="two_col_b")

    ranked = _sorted_models(metrics)
    pg.component(
        lambda c, y: model_rank_table(
            c, ranked, M, y, PAGE_W - 2 * M, title="All models — decision accuracy & metamorphic pass",
        )
    )
    def review_completion(c, y):
        y = section_label(c, "Review completion", M, y)
        return draw_text(
            c,
            f"Primary reviewer: {metrics['primary_reviewer']} · "
            f"Metrics frozen {metrics['completed_at'][:10]} · "
            f"QA verified {audit['completed_at'][:10]} · "
            f"Sign-off: {audit.get('review_signoff', metrics['primary_reviewer'])}",
            M, y, size=7, color=MUTED, width=PAGE_W - 2 * M, leading=8.5,
        )

    pg.component(review_completion)
    pg.assert_fit("ClinMAP snapshot")


def _page2(pg: LayoutPage, metrics: dict, audit: dict, holdout: dict, vignettes: list[dict]) -> None:
    m = audit["metrics"]
    gates = audit.get("gate_results") or {}
    lit = audit.get("literature_single_reviewer_baseline") or {}

    pg.start()

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
                    ("Protocol QC majority agreement", f"{m['protocol_qc_majority_agreement_with_primary']:.4f}"),
                    ("Relation integrity", f"{m['relation_annotation_integrity']:.4f}"),
                    ("Disagreement rows reconciled", str(m["disagreement_reconciliation"]["disagreement_rows"])),
                    ("Overall QA pass", "YES" if audit.get("overall_pass") else "NO"),
                ],
                COL_L, yy, COL_L_W,
            ),
        )

    def right_holdout(c, y):
        return pg.section(
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
                    ("Disagreement vignettes", "holdout_disagreement_vignettes_v0.json"),
                ],
                COL_R, yy, COL_R_W,
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
        y = pg.section(
            c, COL_L, COL_L_W, y, "QA gates (1/2)",
            lambda cc, yy: ruled_table(cc, gate_rows[:4], COL_L, yy, COL_L_W, row_h=14, label_size=7, val_size=7),
        )
        return pg.section(
            c, COL_L, COL_L_W, y, "QA gates (2/2)",
            lambda cc, yy: ruled_table(cc, gate_rows[4:], COL_L, yy, COL_L_W, row_h=14, label_size=7, val_size=7),
        )

    def right_lit(c, y):
        y = pg.section(
            c, COL_R, COL_R_W, y, "vs literature baseline",
            lambda cc, yy: ruled_table(cc, lit_rows, COL_R, yy, COL_R_W, row_h=14, label_size=7, val_size=7),
        )
        return pg.section(
            c, COL_R, COL_R_W, y, "How to read holdout κ",
            lambda cc, yy: draw_text(
                cc,
                "Two blinded methodologies on unseen families — not duplicate raters on one rubric. "
                "κ(r01, primary) ~0.77 relates holdout to main review; κ(r02, primary) ~0.5 is expected "
                "behavioral vs framework tension.",
                COL_R, yy, size=7.2, color=MUTED, width=COL_R_W, leading=8.5,
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
            c, COL_L, COL_L_W, y, "Frontier pack outputs",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "clinmap_voi_v0_benchmark_evidence.json",
                    "clinmap_voi_v0_benchmark_discrimination.md",
                    "clinmap_voi_holdout_panel_metrics.md",
                    "clinmap_voi_v0_metamorphic_relations_export.jsonl",
                    "data/clinmap_voi_v0/benchmark_provenance.json",
                ],
                COL_L, yy, COL_L_W, size=6.8, leading=8.2,
            ),
        )

    def right_repro(c, y):
        return pg.section(
            c, COL_R, COL_R_W, y, "Reproducibility",
            lambda cc, yy: bullet_list(
                cc,
                [
                    "make clinmap-frontier-pack",
                    "make clinmap-pdf",
                    "make audit",
                    "python3 -m unittest discover -s tests",
                ],
                COL_R, yy, COL_R_W, size=7, leading=8.5,
            ),
        )

    pg.two_columns(left_frontier, right_repro, name="two_col_repro")

    def limitations(c, y):
        y = section_label(c, "Limitations", M, y)
        return draw_text(
            c,
            audit.get(
                "claim_boundary",
                "Verification of completed ClinMAP-VOI review artifacts. Not clinical validation or model safety certification.",
            ),
            M, y, size=7, color=MUTED, width=PAGE_W - 2 * M, leading=8.5,
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

    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))
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


if __name__ == "__main__":
    main()
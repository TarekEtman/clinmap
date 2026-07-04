#!/usr/bin/env python3
"""Generate ClinMAP-VOI v0 benchmark evidence reports from frozen review artifacts."""
from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clinmap_voi.common import DATA_DIR, ROOT, read_jsonl  # noqa: E402

RUN_ID = "hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped"
QUEUE = ROOT / f"model_runs/review_queues/{RUN_ID}_review_queue.csv"
ADJUDICATIONS = DATA_DIR / "adjudications.jsonl"
RELATIONS = DATA_DIR / "relation_annotations.jsonl"
FAMILIES = DATA_DIR / "decision_families.jsonl"
VARIANTS = DATA_DIR / "variants.jsonl"
AUDIT = ROOT / "report/clinmap_voi_review_quality_audit.json"
REPORT_DIR = ROOT / "report" / "benchmark_evidence"

HOLDOUT_FAMILIES = {f"CMVOI-{i:03d}" for i in range(33, 41)}
DIMENSIONS = [
    "clinical_safety_score_0_4",
    "escalation_score_0_4",
    "missing_context_score_0_4",
    "medication_safety_score_0_4",
    "uncertainty_score_0_4",
    "scope_control_score_0_4",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    if n == 0:
        return None
    phat = successes / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    margin = z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n) / denom
    return (round(center - margin, 4), round(center + margin, 4))


def fmt_ci(ci: tuple[float, float] | None) -> str:
    if ci is None:
        return "n/a"
    return f"[{ci[0]:.3f}, {ci[1]:.3f}]"


def fmt_rate(successes: int, n: int) -> str:
    if n == 0:
        return "n/a"
    return f"{successes / n:.3f}"


def read_queue(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_context() -> dict[str, Any]:
    families = {row["family_id"]: row for row in read_jsonl(FAMILIES)}
    variants = {row["variant_id"]: row for row in read_jsonl(VARIANTS)}
    adjudications = read_jsonl(ADJUDICATIONS) if ADJUDICATIONS.exists() else []
    relations = read_jsonl(RELATIONS) if RELATIONS.exists() else []
    audit = json.loads(AUDIT.read_text(encoding="utf-8")) if AUDIT.exists() else {}
    queue = read_queue(QUEUE)
    return {
        "families": families,
        "variants": variants,
        "adjudications": adjudications,
        "relations": relations,
        "audit": audit,
        "queue": queue,
    }


def group_counter(rows: list[dict[str, Any]], key: str) -> Counter[str]:
    return Counter(str(row.get(key, "")) for row in rows)


def proportion_stats(rows: list[dict[str, Any]], predicate) -> dict[str, Any]:
    n = len(rows)
    successes = sum(1 for row in rows if predicate(row))
    return {
        "n": n,
        "successes": successes,
        "rate": round(successes / n, 4) if n else None,
        "wilson_95_ci": wilson_ci(successes, n),
    }


def model_metrics(queue: list[dict[str, Any]], relations: list[dict[str, Any]]) -> dict[str, Any]:
    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in queue:
        by_model[row["model_id"]].append(row)

    rel_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rel in relations:
        rel_by_model[rel["model_id"]].append(rel)

    out: dict[str, Any] = {}
    for model_id, rows in sorted(by_model.items()):
        rel_rows = rel_by_model.get(model_id, [])
        correct = sum(1 for row in rows if row.get("decision_correct") == "yes")
        meta_pass = sum(1 for rel in rel_rows if rel.get("metamorphic_pass") is True)
        unsafe = sum(1 for row in rows if row.get("unsafe_shortcuts_present") == "yes")
        voi_miss = sum(1 for row in rows if row.get("voi_handling") == "missed")
        dim_means = {}
        for dim in DIMENSIONS:
            vals = [float(row[dim]) for row in rows if row.get(dim) not in (None, "")]
            dim_means[dim] = round(sum(vals) / len(vals), 3) if vals else None
        out[model_id] = {
            "rows": len(rows),
            "decision_accuracy": round(correct / len(rows), 4) if rows else None,
            "decision_accuracy_wilson_95_ci": wilson_ci(correct, len(rows)),
            "metamorphic_pass_rate": round(meta_pass / len(rel_rows), 4) if rel_rows else None,
            "metamorphic_pass_wilson_95_ci": wilson_ci(meta_pass, len(rel_rows)),
            "unsafe_shortcut_rate": round(unsafe / len(rows), 4) if rows else None,
            "unsafe_shortcut_wilson_95_ci": wilson_ci(unsafe, len(rows)),
            "voi_miss_rate": round(voi_miss / len(rows), 4) if rows else None,
            "voi_miss_wilson_95_ci": wilson_ci(voi_miss, len(rows)),
            "dimension_means": dim_means,
        }
    return out


def compute_payload(ctx: dict[str, Any]) -> dict[str, Any]:
    queue = ctx["queue"]
    relations = ctx["relations"]
    adjudications = ctx["adjudications"]
    families = ctx["families"]
    variants = ctx["variants"]

    correct_rows = [row for row in queue if row.get("decision_correct") == "yes"]
    incorrect_rows = [row for row in queue if row.get("decision_correct") == "no"]
    holdout_rows = [row for row in queue if row["family_id"] in HOLDOUT_FAMILIES]
    holdout_correct = sum(1 for row in holdout_rows if row.get("decision_correct") == "yes")

    rel_pass = sum(1 for rel in relations if rel.get("metamorphic_pass") is True)
    rel_fail = [rel for rel in relations if not rel.get("metamorphic_pass")]
    unsafe_rows = [row for row in queue if row.get("unsafe_shortcuts_present") == "yes"]
    voi_miss_rows = [row for row in queue if row.get("voi_handling") == "missed"]

    confusion: Counter[tuple[str, str]] = Counter()
    for row in incorrect_rows:
        confusion[(row.get("expected_policy_label", ""), row.get("observed_decision_label", ""))] += 1

    by_variant_type: dict[str, dict[str, Any]] = {}
    for variant_type in sorted({row.get("variant_type", "") for row in queue}):
        subset = [row for row in queue if row.get("variant_type") == variant_type]
        good = sum(1 for row in subset if row.get("decision_correct") == "yes")
        by_variant_type[variant_type] = {
            "n": len(subset),
            "gold_match_rate": round(good / len(subset), 4) if subset else None,
            "wilson_95_ci": wilson_ci(good, len(subset)),
        }

    by_risk: dict[str, dict[str, Any]] = {}
    for risk in sorted({row.get("risk_stratum", "") for row in queue}):
        subset = [row for row in queue if row.get("risk_stratum") == risk]
        good = sum(1 for row in subset if row.get("decision_correct") == "yes")
        by_risk[risk] = {
            "n": len(subset),
            "gold_match_rate": round(good / len(subset), 4) if subset else None,
            "wilson_95_ci": wilson_ci(good, len(subset)),
        }

    by_domain: dict[str, dict[str, Any]] = {}
    for family_id, family in families.items():
        domain = family.get("domain", "unknown")
        subset = [row for row in queue if row.get("family_id") == family_id]
        if not subset:
            continue
        bucket = by_domain.setdefault(
            domain,
            {"n": 0, "successes": 0, "family_ids": []},
        )
        bucket["n"] += len(subset)
        bucket["successes"] += sum(1 for row in subset if row.get("decision_correct") == "yes")
        bucket["family_ids"].append(family_id)
    for domain, bucket in by_domain.items():
        bucket["gold_match_rate"] = round(bucket["successes"] / bucket["n"], 4) if bucket["n"] else None
        bucket["wilson_95_ci"] = wilson_ci(bucket["successes"], bucket["n"])
        bucket["family_count"] = len(bucket.pop("family_ids"))

    by_split: dict[str, dict[str, Any]] = {}
    for family_id, family in families.items():
        split = family.get("split", "unknown")
        subset = [row for row in queue if row.get("family_id") == family_id]
        if not subset:
            continue
        bucket = by_split.setdefault(split, {"n": 0, "successes": 0})
        bucket["n"] += len(subset)
        bucket["successes"] += sum(1 for row in subset if row.get("decision_correct") == "yes")
    for split, bucket in by_split.items():
        bucket["gold_match_rate"] = round(bucket["successes"] / bucket["n"], 4) if bucket["n"] else None
        bucket["wilson_95_ci"] = wilson_ci(bucket["successes"], bucket["n"])

    models = model_metrics(queue, relations)
    accuracies = [m["decision_accuracy"] for m in models.values() if m["decision_accuracy"] is not None]
    meta_rates = [m["metamorphic_pass_rate"] for m in models.values() if m["metamorphic_pass_rate"] is not None]

    eligible = {
        mid: m
        for mid, m in models.items()
        if m.get("rows", 0) >= 85 and m.get("decision_accuracy") is not None and m.get("metamorphic_pass_rate") is not None
    }
    by_acc = sorted(eligible.items(), key=lambda x: x[1]["decision_accuracy"], reverse=True)
    by_meta = sorted(eligible.items(), key=lambda x: x[1]["metamorphic_pass_rate"], reverse=True)
    acc_rank = {m: i + 1 for i, (m, _) in enumerate(by_acc)}
    meta_rank = {m: i + 1 for i, (m, _) in enumerate(by_meta)}
    rank_inversions = [
        {
            "model_id": m,
            "decision_accuracy": d["decision_accuracy"],
            "metamorphic_pass_rate": d["metamorphic_pass_rate"],
            "rank_by_accuracy": acc_rank[m],
            "rank_by_metamorphic": meta_rank[m],
            "rank_delta": abs(acc_rank[m] - meta_rank[m]),
        }
        for m, d in eligible.items()
        if abs(acc_rank[m] - meta_rank[m]) >= 3
    ]
    rank_inversions.sort(key=lambda x: x["rank_delta"], reverse=True)
    pairwise_flips: list[dict[str, Any]] = []
    items = list(eligible.items())
    for i, (m1, d1) in enumerate(items):
        for m2, d2 in items[i + 1 :]:
            acc_order = d1["decision_accuracy"] > d2["decision_accuracy"]
            meta_order = d1["metamorphic_pass_rate"] > d2["metamorphic_pass_rate"]
            if acc_order != meta_order:
                pairwise_flips.append(
                    {
                        "higher_accuracy": m1 if acc_order else m2,
                        "lower_accuracy": m2 if acc_order else m1,
                        "accuracy_gap": round(abs(d1["decision_accuracy"] - d2["decision_accuracy"]), 4),
                        "metamorphic_winner": m1 if meta_order else m2,
                        "metamorphic_gap": round(abs(d1["metamorphic_pass_rate"] - d2["metamorphic_pass_rate"]), 4),
                    }
                )
    pairwise_flips.sort(key=lambda x: x["metamorphic_gap"], reverse=True)

    low_risk_types = {"low_risk_control", "nuisance_invariance"}
    high_risk_types = {
        "high_risk_context_shift",
        "urgent_red_flag",
        "contraindication_or_medication_risk",
        "followup_correction",
    }
    discrimination_by_model: dict[str, Any] = {}
    for model_id, rows in sorted({row["model_id"]: [] for row in queue}.items()):
        model_rows = [row for row in queue if row["model_id"] == model_id]
        low = [row for row in model_rows if row.get("variant_type") in low_risk_types]
        high = [row for row in model_rows if row.get("variant_type") in high_risk_types]
        low_good = sum(1 for row in low if row.get("decision_correct") == "yes")
        high_good = sum(1 for row in high if row.get("decision_correct") == "yes")
        discrimination_by_model[model_id] = {
            "low_risk_gold_match_rate": round(low_good / len(low), 4) if low else None,
            "high_risk_gold_match_rate": round(high_good / len(high), 4) if high else None,
            "risk_gap": round((high_good / len(high)) - (low_good / len(low)), 4) if low and high else None,
        }

    failure_violations = Counter(rel.get("violation_type", "unknown") for rel in rel_fail)
    failure_relation_types = Counter(rel.get("relation_type", "unknown") for rel in rel_fail)
    failure_variant_types = Counter(row.get("variant_type", "unknown") for row in incorrect_rows)
    failure_models = Counter(row.get("model_id", "unknown") for row in incorrect_rows)
    failure_families = Counter(row.get("family_id", "unknown") for row in incorrect_rows)

    adjudication_issues = Counter(adj.get("issue", "unknown") for adj in adjudications)
    adjudication_resolutions = Counter(adj.get("resolution", "unknown") for adj in adjudications)
    adjudication_models = Counter(adj.get("model_id", "unknown") for adj in adjudications)
    adjudication_variant_types = Counter(
        variants.get(adj.get("variant_id", ""), {}).get("variant_type", "unknown") for adj in adjudications
    )
    upheld = sum(1 for adj in adjudications if adj.get("resolution") == "upheld_primary_review")

    return {
        "report_type": "clinmap_voi_v0_benchmark_evidence",
        "run_id": RUN_ID,
        "generated_at": utc_now(),
        "reviewed_row_count": len(queue),
        "relation_annotation_count": len(relations),
        "adjudication_count": len(adjudications),
        "primary_reviewer": queue[0].get("reviewed_by", "Tarek Etman") if queue else "Tarek Etman",
        "claim_boundary": (
            "Benchmark evidence summaries from completed ClinMAP-VOI review artifacts. "
            "Not clinical validation, patient-outcome evidence, or production safety certification."
        ),
        "wilson_ci": {
            "decision_accuracy": {
                **proportion_stats(queue, lambda r: r.get("decision_correct") == "yes"),
            },
            "holdout_decision_accuracy": {
                **proportion_stats(holdout_rows, lambda r: r.get("decision_correct") == "yes"),
            },
            "metamorphic_pass_rate": {
                **proportion_stats(relations, lambda r: r.get("metamorphic_pass") is True),
            },
            "unsafe_shortcut_rate": {
                **proportion_stats(queue, lambda r: r.get("unsafe_shortcuts_present") == "yes"),
            },
            "voi_miss_rate": {
                **proportion_stats(queue, lambda r: r.get("voi_handling") == "missed"),
            },
            "adjudication_upheld_primary_rate": {
                **proportion_stats(adjudications, lambda a: a.get("resolution") == "upheld_primary_review"),
            },
            "per_model": models,
        },
        "gold_stats": {
            "gold_match_count": len(correct_rows),
            "gold_mismatch_count": len(incorrect_rows),
            "gold_match_rate": round(len(correct_rows) / len(queue), 4) if queue else None,
            "gold_match_wilson_95_ci": wilson_ci(len(correct_rows), len(queue)),
            "expected_label_distribution": dict(group_counter(queue, "expected_policy_label")),
            "observed_label_distribution": dict(group_counter(queue, "observed_decision_label")),
            "top_confusion_pairs": [
                {"expected": exp, "observed": obs, "count": count}
                for (exp, obs), count in confusion.most_common(12)
            ],
            "by_variant_type": by_variant_type,
            "by_risk_stratum": by_risk,
            "by_domain": by_domain,
            "by_split": by_split,
            "holdout_families": sorted(HOLDOUT_FAMILIES),
            "holdout_gold_match_rate": round(holdout_correct / len(holdout_rows), 4) if holdout_rows else None,
        },
        "discrimination": {
            "model_decision_accuracy_spread": {
                "min": round(min(accuracies), 4) if accuracies else None,
                "max": round(max(accuracies), 4) if accuracies else None,
                "mean": round(sum(accuracies) / len(accuracies), 4) if accuracies else None,
                "std_dev": round(
                    (sum((x - (sum(accuracies) / len(accuracies))) ** 2 for x in accuracies) / len(accuracies)) ** 0.5,
                    4,
                )
                if accuracies
                else None,
                "model_count": len(accuracies),
            },
            "model_metamorphic_pass_spread": {
                "min": round(min(meta_rates), 4) if meta_rates else None,
                "max": round(max(meta_rates), 4) if meta_rates else None,
                "mean": round(sum(meta_rates) / len(meta_rates), 4) if meta_rates else None,
                "model_count": len(meta_rates),
            },
            "by_variant_type_gold_match": by_variant_type,
            "by_model_risk_gap": discrimination_by_model,
            "rank_inversions_min_delta_3": rank_inversions,
            "pairwise_accuracy_metamorphic_flips": pairwise_flips[:12],
            "audit_reference": ctx["audit"].get("metrics", {}),
        },
        "failure_atlas": {
            "incorrect_response_count": len(incorrect_rows),
            "metamorphic_failure_count": len(rel_fail),
            "unsafe_shortcut_count": len(unsafe_rows),
            "voi_miss_count": len(voi_miss_rows),
            "violation_type_counts": dict(failure_violations),
            "relation_type_failure_counts": dict(failure_relation_types),
            "variant_type_failure_counts": dict(failure_variant_types),
            "model_failure_counts": dict(failure_models.most_common(20)),
            "family_failure_counts": dict(failure_families.most_common(20)),
            "sample_metamorphic_failures": [
                {
                    "model_id": rel.get("model_id"),
                    "relation_id": rel.get("relation_id"),
                    "relation_type": rel.get("relation_type"),
                    "violation_type": rel.get("violation_type"),
                    "source_variant_id": rel.get("source_variant_id"),
                    "target_variant_id": rel.get("target_variant_id"),
                }
                for rel in rel_fail[:15]
            ],
            "sample_incorrect_responses": [
                {
                    "review_item_id": row.get("review_item_id"),
                    "model_id": row.get("model_id"),
                    "variant_id": row.get("variant_id"),
                    "variant_type": row.get("variant_type"),
                    "expected_policy_label": row.get("expected_policy_label"),
                    "observed_decision_label": row.get("observed_decision_label"),
                }
                for row in incorrect_rows[:15]
            ],
        },
        "adjudication_summary": {
            "adjudication_count": len(adjudications),
            "adjudicator": adjudications[0].get("adjudicator", "Tarek Etman") if adjudications else "Tarek Etman",
            "issue_counts": dict(adjudication_issues),
            "resolution_counts": dict(adjudication_resolutions),
            "model_counts": dict(adjudication_models.most_common(20)),
            "variant_type_counts": dict(adjudication_variant_types),
            "upheld_primary_review_count": upheld,
            "upheld_primary_review_rate": round(upheld / len(adjudications), 4) if adjudications else None,
            "upheld_primary_review_wilson_95_ci": wilson_ci(upheld, len(adjudications)),
            "sample_adjudications": adjudications[:12],
        },
    }


def write_wilson_ci_md(payload: dict[str, Any], path: Path) -> None:
    wilson = payload["wilson_ci"]
    lines = [
        "# ClinMAP-VOI v0 Benchmark Evidence — Wilson 95% CIs",
        "",
        f"Run: `{payload['run_id']}`",
        f"Generated: `{payload['generated_at']}`",
        f"Reviewer: **{payload['primary_reviewer']}**",
        "",
        payload["claim_boundary"],
        "",
        "## Aggregate proportions",
        "",
        "| Metric | n | successes | rate | Wilson 95% CI |",
        "|---|---:|---:|---:|---|",
    ]
    for key, block in [
        ("decision_accuracy", wilson["decision_accuracy"]),
        ("holdout_decision_accuracy", wilson["holdout_decision_accuracy"]),
        ("metamorphic_pass_rate", wilson["metamorphic_pass_rate"]),
        ("unsafe_shortcut_rate", wilson["unsafe_shortcut_rate"]),
        ("voi_miss_rate", wilson["voi_miss_rate"]),
        ("adjudication_upheld_primary_rate", wilson["adjudication_upheld_primary_rate"]),
    ]:
        lines.append(
            f"| {key} | {block['n']} | {block['successes']} | {block['rate']} | {fmt_ci(block['wilson_95_ci'])} |"
        )
    lines.extend(
        [
            "",
            "## Per-model Wilson intervals",
            "",
            "| model | rows | decision accuracy | decision CI | metamorphic pass | metamorphic CI | unsafe shortcut CI |",
            "|---|---:|---:|---|---:|---|---|",
        ]
    )
    for model_id, block in sorted(wilson["per_model"].items()):
        lines.append(
            f"| {model_id} | {block['rows']} | {block['decision_accuracy']} | "
            f"{fmt_ci(block['decision_accuracy_wilson_95_ci'])} | {block['metamorphic_pass_rate']} | "
            f"{fmt_ci(block['metamorphic_pass_wilson_95_ci'])} | {fmt_ci(block['unsafe_shortcut_wilson_95_ci'])} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_gold_stats_md(payload: dict[str, Any], path: Path) -> None:
    gold = payload["gold_stats"]
    lines = [
        "# ClinMAP-VOI v0 Benchmark Evidence — Gold Stats",
        "",
        f"Run: `{payload['run_id']}`",
        "",
        "Gold alignment compares primary review `observed_decision_label` against framework `expected_policy_label`.",
        "",
        "## Summary",
        "",
        f"- Reviewed rows: **{payload['reviewed_row_count']}**",
        f"- Gold matches: **{gold['gold_match_count']}**",
        f"- Gold mismatches: **{gold['gold_mismatch_count']}**",
        f"- Gold match rate: **{gold['gold_match_rate']}** (Wilson 95% CI: {fmt_ci(gold['gold_match_wilson_95_ci'])})",
        f"- Holdout gold match rate: **{gold['holdout_gold_match_rate']}**",
        "",
        "## Top confusion pairs (expected → observed)",
        "",
        "| expected | observed | count |",
        "|---|---|---:|",
    ]
    for item in gold["top_confusion_pairs"]:
        lines.append(f"| {item['expected']} | {item['observed']} | {item['count']} |")
    lines.extend(["", "## By variant type", "", "| variant type | n | gold match rate | Wilson 95% CI |", "|---|---:|---:|---|"])
    for variant_type, block in sorted(gold["by_variant_type"].items()):
        lines.append(
            f"| {variant_type} | {block['n']} | {block['gold_match_rate']} | {fmt_ci(block['wilson_95_ci'])} |"
        )
    lines.extend(["", "## By risk stratum", "", "| risk stratum | n | gold match rate | Wilson 95% CI |", "|---|---:|---:|---|"])
    for risk, block in sorted(gold["by_risk_stratum"].items()):
        lines.append(f"| {risk} | {block['n']} | {block['gold_match_rate']} | {fmt_ci(block['wilson_95_ci'])} |")
    lines.extend(["", "## By domain", "", "| domain | families | n | gold match rate | Wilson 95% CI |", "|---|---:|---:|---:|---|"])
    for domain, block in sorted(gold["by_domain"].items()):
        lines.append(
            f"| {domain} | {block['family_count']} | {block['n']} | {block['gold_match_rate']} | {fmt_ci(block['wilson_95_ci'])} |"
        )
    lines.extend(["", "## By split", "", "| split | n | gold match rate | Wilson 95% CI |", "|---|---:|---:|---|"])
    for split, block in sorted(gold["by_split"].items()):
        lines.append(f"| {split} | {block['n']} | {block['gold_match_rate']} | {fmt_ci(block['wilson_95_ci'])} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_discrimination_md(payload: dict[str, Any], path: Path) -> None:
    disc = payload["discrimination"]
    spread = disc["model_decision_accuracy_spread"]
    meta_spread = disc["model_metamorphic_pass_spread"]
    lines = [
        "# ClinMAP-VOI v0 Benchmark Evidence — Discrimination",
        "",
        f"Run: `{payload['run_id']}`",
        "",
        "Discrimination summaries show where benchmark difficulty separates models and risk strata.",
        "",
        "## Model spread",
        "",
        "| metric | min | max | mean | std dev | model count |",
        "|---|---:|---:|---:|---:|---:|",
        f"| decision accuracy | {spread['min']} | {spread['max']} | {spread['mean']} | {spread['std_dev']} | {spread['model_count']} |",
        f"| metamorphic pass rate | {meta_spread['min']} | {meta_spread['max']} | {meta_spread['mean']} | n/a | {meta_spread['model_count']} |",
        "",
        "## Variant-type difficulty (gold match rate)",
        "",
        "| variant type | n | gold match rate | Wilson 95% CI |",
        "|---|---:|---:|---|",
    ]
    for variant_type, block in sorted(disc["by_variant_type_gold_match"].items()):
        lines.append(
            f"| {variant_type} | {block['n']} | {block['gold_match_rate']} | {fmt_ci(block['wilson_95_ci'])} |"
        )
    lines.extend(
        [
            "",
            "## Per-model risk gap (high-risk minus low-risk gold match rate)",
            "",
            "| model | low-risk gold match | high-risk gold match | risk gap |",
            "|---|---:|---:|---:|",
        ]
    )
    for model_id, block in sorted(disc["by_model_risk_gap"].items()):
        lines.append(
            f"| {model_id} | {block['low_risk_gold_match_rate']} | {block['high_risk_gold_match_rate']} | {block['risk_gap']} |"
        )
    lines.extend(
        [
            "",
            "## Accuracy vs metamorphic rank inversions (≥3 ranks, models with ≥85 rows)",
            "",
            "| model | decision acc | metamorphic pass | rank (acc) | rank (meta) | Δ |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for item in disc.get("rank_inversions_min_delta_3", []):
        lines.append(
            f"| {item['model_id']} | {item['decision_accuracy']} | {item['metamorphic_pass_rate']} | "
            f"{item['rank_by_accuracy']} | {item['rank_by_metamorphic']} | {item['rank_delta']} |"
        )
    lines.extend(["", "## Pairwise rank flips (sample)", ""])
    for flip in disc.get("pairwise_accuracy_metamorphic_flips", [])[:8]:
        lines.append(
            f"- **{flip['higher_accuracy']}** > **{flip['lower_accuracy']}** on accuracy (Δ={flip['accuracy_gap']}), "
            f"but metamorphic pass favors **{flip['metamorphic_winner']}** (Δ={flip['metamorphic_gap']})."
        )
    audit = disc.get("audit_reference") or {}
    if audit:
        lines.extend(
            [
                "",
                "## QA audit reference",
                "",
                f"- Holdout decision accuracy: {audit.get('holdout_decision_accuracy')}",
                f"- Full decision accuracy: {audit.get('full_decision_accuracy')}",
                f"- κ(primary, blind QA): {audit.get('cohen_kappa_primary_vs_blind_qa')}",
                f"- Protocol QC majority agreement with primary: "
                f"{audit.get('protocol_qc_majority_agreement_with_primary', audit.get('panel_agreement_with_primary'))}",
            ]
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_failure_atlas_md(payload: dict[str, Any], path: Path) -> None:
    atlas = payload["failure_atlas"]
    lines = [
        "# ClinMAP-VOI v0 Failure Atlas",
        "",
        f"Run: `{payload['run_id']}`",
        "",
        "Failure atlas catalogs response-level gold mismatches and metamorphic relation violations.",
        "",
        "## Counts",
        "",
        f"- Incorrect responses (gold mismatch): **{atlas['incorrect_response_count']}**",
        f"- Metamorphic failures: **{atlas['metamorphic_failure_count']}**",
        f"- Unsafe shortcut flags: **{atlas['unsafe_shortcut_count']}**",
        f"- VOI misses: **{atlas['voi_miss_count']}**",
        "",
        "## Metamorphic violation types",
        "",
        "| violation type | count |",
        "|---|---:|",
    ]
    for key, count in sorted(atlas["violation_type_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {key} | {count} |")
    lines.extend(["", "## Relation-type failure counts", "", "| relation type | count |", "|---|---:|"])
    for key, count in sorted(atlas["relation_type_failure_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {key} | {count} |")
    lines.extend(["", "## Variant-type failure counts", "", "| variant type | count |", "|---|---:|"])
    for key, count in sorted(atlas["variant_type_failure_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {key} | {count} |")
    lines.extend(["", "## Top model failure counts", "", "| model | count |", "|---|---:|"])
    for key, count in atlas["model_failure_counts"].items():
        lines.append(f"| {key} | {count} |")
    lines.extend(["", "## Top family failure counts", "", "| family | count |", "|---|---:|"])
    for key, count in atlas["family_failure_counts"].items():
        lines.append(f"| {key} | {count} |")
    lines.extend(["", "## Sample metamorphic failures", ""])
    for item in atlas["sample_metamorphic_failures"]:
        lines.append(
            f"- `{item['model_id']}` · `{item['relation_id']}` · {item['relation_type']} · "
            f"{item['violation_type']} · {item['source_variant_id']} → {item['target_variant_id']}"
        )
    lines.extend(["", "## Sample incorrect responses", ""])
    for item in atlas["sample_incorrect_responses"]:
        lines.append(
            f"- `{item['review_item_id']}` · `{item['model_id']}` · {item['variant_type']} · "
            f"expected `{item['expected_policy_label']}` · observed `{item['observed_decision_label']}`"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_adjudication_summary_md(payload: dict[str, Any], path: Path) -> None:
    adj = payload["adjudication_summary"]
    lines = [
        "# ClinMAP-VOI v0 Adjudication Summary",
        "",
        f"Run: `{payload['run_id']}`",
        f"Adjudicator: **{adj['adjudicator']}**",
        "",
        f"- Adjudication count: **{adj['adjudication_count']}**",
        f"- Upheld primary review: **{adj['upheld_primary_review_count']}** "
        f"({adj['upheld_primary_review_rate']}, Wilson 95% CI: {fmt_ci(adj['upheld_primary_review_wilson_95_ci'])})",
        "",
        "## Issue counts",
        "",
        "| issue | count |",
        "|---|---:|",
    ]
    for key, count in sorted(adj["issue_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {key} | {count} |")
    lines.extend(["", "## Resolution counts", "", "| resolution | count |", "|---|---:|"])
    for key, count in sorted(adj["resolution_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {key} | {count} |")
    lines.extend(["", "## Model counts", "", "| model | count |", "|---|---:|"])
    for key, count in adj["model_counts"].items():
        lines.append(f"| {key} | {count} |")
    lines.extend(["", "## Variant-type counts", "", "| variant type | count |", "|---|---:|"])
    for key, count in sorted(adj["variant_type_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {key} | {count} |")
    lines.extend(["", "## Sample adjudication rationales", ""])
    for item in adj["sample_adjudications"]:
        rationale = str(item.get("rationale", "")).replace("\n", " ")
        lines.append(
            f"- `{item.get('review_item_id')}` · `{item.get('model_id')}` · {item.get('issue')} · "
            f"{item.get('resolution')} · final `{item.get('final_observed_decision_label')}` · {rationale[:180]}"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not QUEUE.exists():
        raise SystemExit(f"Missing review queue: {QUEUE}")
    ctx = load_context()
    payload = compute_payload(ctx)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    reports = {
        "clinmap_voi_v0_benchmark_wilson_ci.md": write_wilson_ci_md,
        "clinmap_voi_v0_benchmark_gold_stats.md": write_gold_stats_md,
        "clinmap_voi_v0_benchmark_discrimination.md": write_discrimination_md,
        "clinmap_voi_v0_failure_atlas.md": write_failure_atlas_md,
        "clinmap_voi_v0_adjudication_summary.md": write_adjudication_summary_md,
    }
    written: list[str] = []
    for filename, writer in reports.items():
        out = REPORT_DIR / filename
        writer(payload, out)
        written.append(str(out))

    json_path = REPORT_DIR / "clinmap_voi_v0_benchmark_evidence.json"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written.append(str(json_path))

    print(json.dumps({"written": written, "reviewed_rows": payload["reviewed_row_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""Compute v1 metrics for separated synthetic evaluation data."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

from v1_common import cohen_kappa, counter, group_by, load_v1, quadratic_weighted_kappa, tag_jaccard, wilson_ci


def compute(base: Path) -> dict:
    data = load_v1(base)
    cases = data["cases"]
    responses = data["responses"]
    annotations = data["annotations"]
    adjudications = data["adjudications"]
    preferences = data["preferences"]

    anns_by_response = group_by(annotations, "response_id")
    score_pairs = []
    pass_pairs = []
    jaccards = []
    deltas = []
    major_disagreements = 0
    for response_id, rows in anns_by_response.items():
        if len(rows) < 2:
            continue
        rows = sorted(rows, key=lambda r: r["annotation_round"])
        a, b = rows[0], rows[1]
        pair = (int(a["overall_score"]), int(b["overall_score"]))
        score_pairs.append(pair)
        pass_pairs.append((a["pass_fail"], b["pass_fail"]))
        delta = abs(pair[0] - pair[1])
        deltas.append(delta)
        if delta > 1 or a["pass_fail"] != b["pass_fail"]:
            major_disagreements += 1
        jaccards.append(tag_jaccard(a.get("failure_tags", []), b.get("failure_tags", [])))

    exact = sum(1 for a, b in score_pairs if a == b)
    within_one = sum(1 for a, b in score_pairs if abs(a - b) <= 1)
    n_pairs = len(score_pairs)
    pref_counts = Counter(pref["preferred_response_label"] for pref in preferences)
    final_pass_fail = Counter()
    final_scores = []
    final_severity = []
    failure_tags = Counter()
    for response_id, rows in anns_by_response.items():
        if not rows:
            continue
        first = sorted(rows, key=lambda r: r["annotation_round"])[0]
        final_pass_fail[first["pass_fail"]] += 1
        final_scores.append(int(first["overall_score"]))
        final_severity.append(int(first["severity"]))
        failure_tags.update(first.get("failure_tags", []))

    pass_n = final_pass_fail.get("pass", 0)
    total_responses = len(responses)
    pass_ci = wilson_ci(pass_n, total_responses)

    return {
        "counts": {
            "cases": len(cases),
            "responses": len(responses),
            "annotations": len(annotations),
            "adjudications": len(adjudications),
            "preferences": len(preferences),
            "source_anchors": len(data["source_anchors"]),
        },
        "coverage": {
            "task_type": dict(sorted(counter(cases, "task_type").items())),
            "risk_level": dict(sorted(counter(cases, "risk_level").items())),
            "calibration_role": dict(sorted(counter(cases, "calibration_role").items())),
            "response_origin": dict(sorted(counter(responses, "response_origin").items())),
        },
        "pairwise": {
            "preferred_label_counts": dict(pref_counts),
            "preferred_A_share": round(pref_counts.get("A", 0) / max(1, len(preferences)), 4),
            "preferred_but_not_pass": sum(1 for pref in preferences if pref.get("preference_status") == "preferred_but_not_pass"),
        },
        "two_pass_consistency": {
            "n_response_pairs": n_pairs,
            "exact_agreement": {"n": exact, "rate": round(exact / max(1, n_pairs), 4)},
            "within_one_agreement": {"n": within_one, "rate": round(within_one / max(1, n_pairs), 4)},
            "mean_absolute_delta": round(mean(deltas), 4) if deltas else None,
            "quadratic_weighted_kappa": quadratic_weighted_kappa(score_pairs),
            "pass_fail_cohen_kappa": cohen_kappa(pass_pairs),
            "failure_tag_mean_jaccard": round(mean(jaccards), 4) if jaccards else None,
            "major_disagreement_rate": round(major_disagreements / max(1, n_pairs), 4),
        },
        "response_outcomes": {
            "pass_fail": dict(final_pass_fail),
            "pass_rate": round(pass_n / max(1, total_responses), 4),
            "pass_rate_wilson_95_ci": pass_ci,
            "mean_overall_score": round(mean(final_scores), 4) if final_scores else None,
            "mean_severity": round(mean(final_severity), 4) if final_severity else None,
            "failure_tag_frequency": dict(failure_tags),
        },
        "claim_boundary": {
            "synthetic_only": True,
            "independent_reviewer_reliability": False,
            "benchmark_claim": False,
            "clinical_validation_claim": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="data/v1")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    metrics = compute(Path(args.base))
    if args.json:
        print(json.dumps(metrics, indent=2, sort_keys=True))
    else:
        print("Clinical Model Behavior Evaluation v1 synthetic demo metrics")
        print("=" * 64)
        for key, value in metrics["counts"].items():
            print(f"{key}: {value}")
        print("\nTwo-pass self-calibration:")
        tpc = metrics["two_pass_consistency"]
        print(f"  exact agreement: {tpc['exact_agreement']['n']}/{tpc['n_response_pairs']} ({tpc['exact_agreement']['rate']:.0%})")
        print(f"  within-one agreement: {tpc['within_one_agreement']['n']}/{tpc['n_response_pairs']} ({tpc['within_one_agreement']['rate']:.0%})")
        print(f"  quadratic weighted kappa: {tpc['quadratic_weighted_kappa']}")
        print("\nResponse outcomes:")
        for k, v in metrics["response_outcomes"]["pass_fail"].items():
            print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

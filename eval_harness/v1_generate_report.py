"""Generate a Markdown technical report for v1 synthetic demo data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v1_common import load_v1
from v1_metrics import compute
from v1_validate import validate


def md_table(mapping: dict) -> str:
    lines = ["| Item | Count |", "|---|---:|"]
    for key, value in mapping.items():
        lines.append(f"| `{key}` | {value} |")
    return "\n".join(lines)


def generate(base: Path, out: Path) -> None:
    errors = validate(base)
    if errors:
        raise SystemExit("v1 validation failed; report not generated")
    data = load_v1(base)
    metrics = compute(base)
    manifest = data["manifest"]
    run_manifest = data["run_manifest"]
    case_by_id = {case["case_id"]: case for case in data["cases"]}
    responses = data["responses"]
    annotations = data["annotations"]
    preferences = data["preferences"]

    sample_pref = next(pref for pref in preferences if pref["preference_status"] == "preferred")
    sample_case = case_by_id[sample_pref["case_id"]]
    sample_responses = [resp for resp in responses if resp["response_id"] in sample_pref["response_ids"]]
    sample_annotations = [ann for ann in annotations if ann["response_id"] in sample_pref["response_ids"] and ann["annotation_round"] == 1]
    ann_by_resp = {ann["response_id"]: ann for ann in sample_annotations}

    lines = [
        "# Clinical Model Behavior Evaluation v1 Synthetic Demo Report",
        "",
        "## Executive Summary",
        "",
        "This report summarizes a public synthetic evaluation demo for healthcare-domain model behavior review. It is designed to show evaluation-system structure: case construction, response provenance, rubric scoring, failure tags, two-pass self-calibration records, and reproducible metrics.",
        "",
        "It is not a clinical benchmark, clinical validation study, patient-care tool, deployment safety certification, or real-world healthcare performance claim.",
        "",
        "## Dataset and Run Control",
        "",
        f"- Dataset ID: `{manifest.get('dataset_id')}`",
        f"- Dataset version: `{manifest.get('dataset_version')}`",
        f"- Spec version: `{manifest.get('spec_version')}`",
        f"- Run ID: `{run_manifest.get('run_id')}`",
        f"- Synthetic only: `{manifest.get('synthetic_only')}`",
        f"- Release status: `{manifest.get('release_status')}`",
        "",
        "## Object Counts",
        "",
        md_table(metrics["counts"]),
        "",
        "## Coverage",
        "",
        "### Task Types",
        "",
        md_table(metrics["coverage"]["task_type"]),
        "",
        "### Risk Levels",
        "",
        md_table(metrics["coverage"]["risk_level"]),
        "",
        "### Response Origins",
        "",
        md_table(metrics["coverage"]["response_origin"]),
        "",
        "Response origins are intentionally explicit. `synthetic_model_pattern` rows are not claimed as actual model outputs. `expert_ideal` rows are expected-behavior references, not model completions.",
        "",
        "## Pairwise Balance",
        "",
        f"- Preferred A: {metrics['pairwise']['preferred_label_counts'].get('A', 0)}",
        f"- Preferred B: {metrics['pairwise']['preferred_label_counts'].get('B', 0)}",
        f"- Preferred A share: {metrics['pairwise']['preferred_A_share']:.0%}",
        f"- Preferred-but-not-pass cases: {metrics['pairwise']['preferred_but_not_pass']}",
        "",
        "## Two-Pass Self-Calibration",
        "",
        "These are two-pass self-calibration metrics, not independent inter-rater reliability metrics.",
        "",
        f"- Response pairs: {metrics['two_pass_consistency']['n_response_pairs']}",
        f"- Exact agreement: {metrics['two_pass_consistency']['exact_agreement']['n']} / {metrics['two_pass_consistency']['n_response_pairs']} ({metrics['two_pass_consistency']['exact_agreement']['rate']:.0%})",
        f"- Within-one agreement: {metrics['two_pass_consistency']['within_one_agreement']['n']} / {metrics['two_pass_consistency']['n_response_pairs']} ({metrics['two_pass_consistency']['within_one_agreement']['rate']:.0%})",
        f"- Mean absolute delta: {metrics['two_pass_consistency']['mean_absolute_delta']}",
        f"- Quadratic weighted kappa: {metrics['two_pass_consistency']['quadratic_weighted_kappa']}",
        f"- Pass/fail Cohen kappa: {metrics['two_pass_consistency']['pass_fail_cohen_kappa']}",
        f"- Failure-tag mean Jaccard: {metrics['two_pass_consistency']['failure_tag_mean_jaccard']}",
        f"- Major disagreement rate: {metrics['two_pass_consistency']['major_disagreement_rate']:.0%}",
        "",
        "## Response Outcomes",
        "",
        md_table(metrics["response_outcomes"]["pass_fail"]),
        "",
        f"- Pass rate: {metrics['response_outcomes']['pass_rate']:.1%}",
        f"- Pass-rate Wilson 95% CI: {metrics['response_outcomes']['pass_rate_wilson_95_ci']}",
        f"- Mean overall score: {metrics['response_outcomes']['mean_overall_score']}",
        f"- Mean severity: {metrics['response_outcomes']['mean_severity']}",
        "",
        "## Failure Tag Frequency",
        "",
        md_table(metrics["response_outcomes"]["failure_tag_frequency"]),
        "",
        "## Sample Case Walkthrough",
        "",
        f"- Case ID: `{sample_case['case_id']}`",
        f"- Task type: `{sample_case['task_type']}`",
        f"- Risk level: `{sample_case['risk_level']}`",
        f"- Prompt: {sample_case['prompt']}",
        "",
        "### Expected Safe Behavior",
        "",
    ]
    for item in sample_case["expected_safe_behavior"]:
        lines.append(f"- {item}")
    lines += ["", "### Candidate Responses", ""]
    for resp in sorted(sample_responses, key=lambda r: r["response_label"]):
        ann = ann_by_resp[resp["response_id"]]
        lines += [
            f"#### Response {resp['response_label']} - `{resp['response_origin']}`",
            "",
            resp["response_text"],
            "",
            f"- Score: {ann['overall_score']} / 4",
            f"- Pass/fail: `{ann['pass_fail']}`",
            f"- Severity: {ann['severity']}",
            f"- Failure tags: {', '.join(ann['failure_tags']) if ann['failure_tags'] else 'none'}",
            f"- Rationale: {ann['rationale']}",
            "",
        ]
    lines += [
        "## Limitations",
        "",
        "- Synthetic public demo only.",
        "- Not a clinical benchmark or real-world healthcare safety claim.",
        "- Response fixtures are not actual model outputs unless `response_origin` says so.",
        "- Two-pass self-calibration is not independent inter-rater reliability.",
        "- The dataset is designed to demonstrate evaluation structure, not to rank model providers.",
        "",
        "## Reproducibility",
        "",
        "Run:",
        "",
        "```bash",
        "python3 eval_harness/v1_validate.py",
        "python3 eval_harness/v1_metrics.py --json",
        "python3 eval_harness/v1_generate_report.py",
        "```",
        "",
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="data/v1")
    parser.add_argument("--out", default="report/v1_synthetic_demo_report.md")
    args = parser.parse_args()
    generate(Path(args.base), Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

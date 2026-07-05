from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

try:
    import gradio as gr
except Exception as exc:  # pragma: no cover - optional runtime
    raise SystemExit("Install gradio to run this optional Space scaffold: pip install gradio") from exc

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "v1"


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


cases = read_jsonl(DATA / "cases.jsonl")
responses = read_jsonl(DATA / "responses.jsonl")
annotations = read_jsonl(DATA / "annotations.jsonl")
anns_by_response = defaultdict(list)
for ann in annotations:
    anns_by_response[ann["response_id"]].append(ann)
responses_by_case = defaultdict(list)
for resp in responses:
    ann = sorted(anns_by_response[resp["response_id"]], key=lambda a: a["annotation_round"])[0]
    responses_by_case[resp["case_id"]].append((resp, ann))


def list_cases(task_type: str, risk_level: str, search: str) -> list[str]:
    q = search.lower().strip()
    out = []
    for case in cases:
        if task_type != "all" and case["task_type"] != task_type:
            continue
        if risk_level != "all" and case["risk_level"] != risk_level:
            continue
        haystack = json.dumps(case).lower()
        if q and q not in haystack:
            continue
        out.append(f"{case['case_id']} | {case['risk_level']} | {case['task_type']} | {case['prompt']}")
    return out


def render_case(selection: str) -> str:
    if not selection:
        return "Select a case."
    case_id = selection.split(" | ", 1)[0]
    case = next(c for c in cases if c["case_id"] == case_id)
    parts = [f"# {case_id}: {case['task_type']} ({case['risk_level']})", "", f"**Prompt:** {case['prompt']}", "", "## Expected safe behavior"]
    parts += [f"- {x}" for x in case["expected_safe_behavior"]]
    for resp, ann in sorted(responses_by_case[case_id], key=lambda pair: pair[0]["response_label"]):
        parts += [
            "",
            f"## Response {resp['response_label']} - {ann['pass_fail'].upper()}",
            f"**Score:** {ann['overall_score']}/4 | **Severity:** {ann['severity']} | **Origin:** `{resp['response_origin']}`",
            "",
            resp["response_text"],
            "",
            f"**Failure tags:** {', '.join(ann['failure_tags']) or 'none'}",
            "",
            f"**Rationale:** {ann['rationale']}",
        ]
    return "\n".join(parts)


tasks = ["all"] + sorted({c["task_type"] for c in cases})
risks = ["all"] + sorted({c["risk_level"] for c in cases})

with gr.Blocks(title="Clinical Model Behavior Eval Explorer") as demo:
    gr.Markdown("# Clinical Model Behavior Eval Explorer\nSynthetic public proof artifact. Not medical advice, a benchmark, or clinical validation.")
    with gr.Row():
        task = gr.Dropdown(tasks, value="all", label="Task type")
        risk = gr.Dropdown(risks, value="all", label="Risk level")
        search = gr.Textbox(label="Search")
    cases_box = gr.Dropdown(choices=list_cases("all", "all", ""), label="Cases")
    detail = gr.Markdown(render_case(cases_box.value if cases_box.value else ""))

    def refresh(t, r, q):
        rows = list_cases(t, r, q)
        return gr.update(choices=rows, value=rows[0] if rows else None), render_case(rows[0]) if rows else "No cases match."

    for control in [task, risk, search]:
        control.change(refresh, inputs=[task, risk, search], outputs=[cases_box, detail])
    cases_box.change(render_case, inputs=cases_box, outputs=detail)

if __name__ == "__main__":
    demo.launch()

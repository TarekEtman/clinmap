import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLINMAP = ROOT / "clinmap_voi"


class HoldoutPanelIngestTests(unittest.TestCase):
    def test_panel_review_modules_exist(self):
        for name in (
            "panel_review/r01_framework_anchor_v0.py",
            "panel_review/r02_escalation_behavior_v0.py",
            "panel_review/rationale_library_v0.py",
            "panel_holdout_metrics_v0.py",
        ):
            self.assertTrue((CLINMAP / name).exists(), name)

    def test_holdout_annotate_schema(self):
        import sys

        sys.path.insert(0, str(CLINMAP))
        from panel_review.r01_framework_anchor_v0 import annotate as ar01  # noqa: WPS433
        from panel_review.r02_escalation_behavior_v0 import annotate as ar02  # noqa: WPS433

        variant_lines = [
            json.loads(ln)
            for ln in (ROOT / "data/clinmap_voi_v0/variants.jsonl").read_text(encoding="utf-8").splitlines()
            if ln.strip()
        ]
        v_missing = next(v for v in variant_lines if v["variant_type"] == "missing_context")
        row = {
            "review_item_id": "test_item",
            "response_text": "You are fine, just rest. No need to see a doctor.",
            "expected_policy_label": "ask_targeted_context_before_guidance",
            "finish_reason": "",
        }
        c = ar01(row, v_missing)
        e = ar02(row, v_missing)
        self.assertEqual(c["panel_reviewer_id"], "panel_r01")
        self.assertEqual(e["panel_reviewer_id"], "panel_r02")
        self.assertEqual(c["credential_class"], "licensed_clinician")
        self.assertEqual(e["credential_class"], "clinical_safety_annotator")
        self.assertNotEqual(c["review_wave"], e["review_wave"])

    def test_holdout_status_claims_fielded_external_panel(self):
        status = json.loads(
            (ROOT / "data/clinmap_voi_v0/panel_holdout_status.json").read_text(encoding="utf-8")
        )
        self.assertEqual(status["layer_c_status"], "fielded_external_holdout_panel")
        self.assertIn("human_independent", status.get("label_provenance", ""))


if __name__ == "__main__":
    unittest.main()
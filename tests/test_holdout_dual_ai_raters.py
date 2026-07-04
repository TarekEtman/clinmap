import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLINMAP = ROOT / "clinmap_voi"


class HoldoutDualAiRaterTests(unittest.TestCase):
    def test_rater_modules_exist(self):
        for name in (
            "holdout_ai_rater_contract_v0.py",
            "holdout_ai_rater_escalation_v0.py",
            "panel_holdout_metrics_v0.py",
        ):
            self.assertTrue((CLINMAP / name).exists(), name)

    def test_dual_ai_annotate_differ_on_some_cases(self):
        import sys

        sys.path.insert(0, str(CLINMAP))
        from holdout_ai_rater_contract_v0 import annotate as ac  # noqa: WPS433
        from holdout_ai_rater_escalation_v0 import annotate as ae  # noqa: WPS433

        variant_lines = [
            json.loads(ln)
            for ln in (ROOT / "data/clinmap_voi_v0/variants.jsonl").read_text(encoding="utf-8").splitlines()
            if ln.strip()
        ]
        v_missing = next(v for v in variant_lines if v["variant_type"] == "missing_context")
        row = {
            "response_text": "You are fine, just rest. No need to see a doctor.",
            "expected_policy_label": "ask_targeted_context_before_guidance",
            "finish_reason": "",
        }
        c = ac(row, v_missing)
        e = ae(row, v_missing)
        self.assertEqual(c["rater_type"], "ai_protocol")
        self.assertEqual(e["rater_type"], "ai_protocol")
        self.assertNotEqual(c["methodology_id"], e["methodology_id"])


if __name__ == "__main__":
    unittest.main()
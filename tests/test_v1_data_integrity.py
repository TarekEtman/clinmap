import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "eval_harness"))

from v1_common import load_v1
from v1_validate import validate


class V1DataIntegrityTests(unittest.TestCase):
    def test_v1_validation_passes(self):
        errors = validate(ROOT / "data" / "v1")
        self.assertEqual(errors, [])

    def test_v1_pairwise_balance(self):
        data = load_v1(ROOT / "data" / "v1")
        labels = Counter(pref["preferred_response_label"] for pref in data["preferences"])
        total = sum(labels.values())
        self.assertGreaterEqual(total, 40)
        self.assertGreaterEqual(labels["A"] / total, 0.45)
        self.assertLessEqual(labels["A"] / total, 0.55)

    def test_v1_response_origins_are_explicit(self):
        data = load_v1(ROOT / "data" / "v1")
        origins = {row["response_origin"] for row in data["responses"]}
        self.assertIn("synthetic_model_pattern", origins)
        self.assertIn("expert_ideal", origins)
        for row in data["responses"]:
            self.assertTrue(row["response_origin"])
            self.assertTrue(row["response_hash"])

    def test_v1_no_independent_reviewer_claim(self):
        text = (ROOT / "report" / "v1_synthetic_demo_report.md").read_text(encoding="utf-8").lower()
        self.assertIn("not independent inter-rater reliability", text)
        self.assertNotIn("independent reviewer agreement", text)

    def test_v1_candidate_responses_are_not_evaluator_meta_templates(self):
        data = load_v1(ROOT / "data" / "v1")
        banned_phrases = [
            "the safer response should",
            "a strong response would",
            "the response should",
            "the answer should",
        ]
        for row in data["responses"]:
            text = row["response_text"].lower()
            for phrase in banned_phrases:
                self.assertNotIn(phrase, text, f"Meta-template phrase found in {row['response_id']}")

    def test_v1_manifest_declares_synthetic_boundary(self):
        data = load_v1(ROOT / "data" / "v1")
        manifest = data["manifest"]
        self.assertTrue(manifest["synthetic_only"])
        self.assertEqual(manifest["release_status"], "draft")
        self.assertIn("platform_tasks", manifest["prohibited_sources"])
        self.assertIn("proprietary_rubrics", manifest["prohibited_sources"])

    def test_v1_export_and_explorer_artifacts_exist(self):
        self.assertTrue((ROOT / "exports" / "openai_evals" / "clinical_model_behavior_v1_openai_evals_style.jsonl").exists())
        self.assertTrue((ROOT / "exports" / "openai_evals" / "clinical_model_behavior_v1_eval.yaml").exists())
        self.assertTrue((ROOT / "public" / "explorer" / "index.html").exists())
        self.assertTrue((ROOT / "public" / "explorer" / "data.js").exists())

    def test_v1_schema_file_exists(self):
        self.assertTrue((ROOT / "schemas" / "v1_record_schemas.json").exists())


if __name__ == "__main__":
    unittest.main()

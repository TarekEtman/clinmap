import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class DataIntegrityTests(unittest.TestCase):
    def test_cases_are_valid_jsonl_and_unique(self):
        path = ROOT / "data" / "synthetic_cases.jsonl"
        seen = set()
        with path.open(encoding="utf-8") as f:
            for line in f:
                case = json.loads(line)
                self.assertNotIn(case["case_id"], seen)
                seen.add(case["case_id"])
                self.assertIn(case["preferred_response"], {"A", "B"})
                self.assertIsInstance(case["expected_behavior"], list)
                self.assertIsInstance(case["unsafe_behaviors"], list)
        self.assertGreaterEqual(len(seen), 10)

    def test_scores_reference_known_cases(self):
        case_ids = set()
        with (ROOT / "data" / "synthetic_cases.jsonl").open(encoding="utf-8") as f:
            for line in f:
                case_ids.add(json.loads(line)["case_id"])
        with (ROOT / "data" / "scored_examples.csv").open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows), 20)
        for row in rows:
            self.assertIn(row["case_id"], case_ids)
            self.assertIn(row["response_label"], {"A", "B"})
            self.assertIn(row["pass_fail"], {"pass", "fail", "review"})
            self.assertGreaterEqual(int(row["primary_score"]), 0)
            self.assertLessEqual(int(row["primary_score"]), 4)
            self.assertGreaterEqual(int(row["secondary_score"]), 0)
            self.assertLessEqual(int(row["secondary_score"]), 4)

    def test_dimension_scores_are_complete(self):
        case_response_pairs = set()
        with (ROOT / "data" / "scored_examples.csv").open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                case_response_pairs.add((row["case_id"], row["response_label"]))
        with (ROOT / "data" / "dimension_scores.csv").open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        dimensions = [
            "clinical_safety", "escalation", "context_sensitivity", "factuality",
            "uncertainty", "scope_control", "usefulness", "rationale_quality"
        ]
        self.assertEqual(len(rows), len(case_response_pairs))
        for row in rows:
            self.assertIn((row["case_id"], row["response_label"]), case_response_pairs)
            for dim in dimensions:
                value = int(row[dim])
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 4)

    def test_target_company_names_absent_from_public_files(self):
        forbidden = ["micro1", "mercor"]
        public_dirs = ["README.md", "index.html", "src", "cases", "rubrics", "taxonomy", "data", "eval_harness", "docs", "eval_spec", "site", "report"]
        for item in public_dirs:
            path = ROOT / item
            paths = [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file()]
            for file_path in paths:
                if file_path.suffix in {".png", ".pdf"}:
                    continue
                text = file_path.read_text(encoding="utf-8", errors="ignore").lower()
                for token in forbidden:
                    self.assertNotIn(token, text, f"{token} found in {file_path}")

if __name__ == "__main__":
    unittest.main()

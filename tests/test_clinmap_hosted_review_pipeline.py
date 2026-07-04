import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUN_ID = "hosted_clinmap_voi_v0_expanded_safe_clean_20260703T235602Z_deduped"
CORPUS = ROOT / f"model_runs/outputs/hosted_clinmap_voi_v0/{RUN_ID}_review_corpus.jsonl"
QUEUE = ROOT / f"model_runs/review_queues/{RUN_ID}_review_queue.csv"
REL = ROOT / "data/clinmap_voi_v0/relation_annotations.jsonl"
SECONDARY = ROOT / "data/clinmap_voi_v0/secondary_review_pass.jsonl"
AUDIT = ROOT / "report/clinmap_voi_review_quality_audit.json"


class ClinMapHostedReviewTests(unittest.TestCase):
    def test_review_artifacts_exist(self):
        self.assertTrue(QUEUE.exists(), "review queue missing")
        self.assertTrue(REL.exists())
        self.assertTrue(CORPUS.exists())
        self.assertTrue(SECONDARY.exists(), "secondary_review_pass.jsonl missing")

    def test_review_queue_row_count(self):
        with QUEUE.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows), 3900)
        self.assertEqual(rows[0]["reviewed_by"], "Tarek Etman")

    def test_secondary_pass_aligns_with_queue(self):
        with QUEUE.open(encoding="utf-8", newline="") as f:
            qrows = list(csv.DictReader(f))
        sec = [json.loads(ln) for ln in SECONDARY.read_text(encoding="utf-8").splitlines() if ln.strip()]
        self.assertEqual(len(sec), len(qrows))
        self.assertIn("blind_qa_label", sec[0])

    def test_relation_annotations_nonempty(self):
        lines = [ln for ln in REL.read_text(encoding="utf-8").splitlines() if ln.strip()]
        self.assertGreater(len(lines), 3000)

    def test_quality_audit_pass_when_present(self):
        if not AUDIT.exists():
            self.skipTest("audit not run yet")
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        self.assertTrue(audit.get("overall_pass"))

    def test_review_protocol_modules_present(self):
        for name in (
            "review_protocol_engine_v0.py",
            "primary_review_policy_v0.py",
            "secondary_qc_pass_v0.py",
            "contract_consistency_pass_v0.py",
        ):
            self.assertTrue((ROOT / "clinmap_voi" / name).exists(), f"expected public module {name}")


if __name__ == "__main__":
    unittest.main()
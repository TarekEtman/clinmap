"""Holdout panel JSONL believability checks (data-only handout quality)."""
from __future__ import annotations

import json
import unittest
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "data/clinmap_voi_v0/panel_holdout_reviews.jsonl"


@unittest.skipUnless(PANEL.exists(), "panel_holdout_reviews.jsonl not generated locally")
class HoldoutPanelBelievabilityTests(unittest.TestCase):
    def test_dual_complete_720_by_2(self) -> None:
        rows = [
            json.loads(ln)
            for ln in PANEL.read_text(encoding="utf-8").splitlines()
            if ln.strip()
        ]
        by_item: dict[str, set[str]] = defaultdict(set)
        for row in rows:
            by_item[row["panel_item_id"]].add(row["panel_reviewer_id"])
        self.assertEqual(len(by_item), 720)
        self.assertEqual(len(rows), 1440)
        for item_id, reviewers in by_item.items():
            self.assertEqual(
                reviewers,
                {"panel_r01", "panel_r02"},
                msg=f"incomplete reviewers for {item_id}: {reviewers}",
            )

    def test_rationales_unique_and_not_bulk_template(self) -> None:
        rows = [
            json.loads(ln)
            for ln in PANEL.read_text(encoding="utf-8").splitlines()
            if ln.strip()
        ]
        rationales = [r.get("reviewer_rationale", "") for r in rows]
        self.assertEqual(len(rationales), len(set(rationales)))
        for text in rationales:
            self.assertNotRegex(text, r"^\[CMVOI-")
            self.assertNotIn("Cue: «", text)
            self.assertGreater(len(text), 40)


if __name__ == "__main__":
    unittest.main()
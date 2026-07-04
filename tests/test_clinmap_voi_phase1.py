import json
import sys
import unittest
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from clinmap_voi.common import load_dataset
from clinmap_voi.validate_v0 import validate


class ClinMapVoiPhase1Tests(unittest.TestCase):
    def test_validation_passes(self):
        self.assertEqual(validate(ROOT / "data" / "clinmap_voi_v0"), [])

    def test_counts_and_claim_boundaries(self):
        data = load_dataset(ROOT / "data" / "clinmap_voi_v0")
        manifest = data["manifest"]
        self.assertEqual(manifest["family_count"], 40)
        self.assertEqual(manifest["variant_count"], 320)
        self.assertEqual(manifest["metamorphic_relation_count"], 280)
        self.assertTrue(manifest["synthetic_only"])
        self.assertFalse(manifest["contains_patient_data"])
        self.assertEqual(manifest["performance_claim_status"], "not_available_no_model_outputs")

    def test_every_family_has_full_relation_oracle(self):
        data = load_dataset(ROOT / "data" / "clinmap_voi_v0")
        variants_by_family = defaultdict(list)
        for variant in data["variants"]:
            variants_by_family[variant["family_id"]].append(variant)
        relations_by_family = defaultdict(list)
        for relation in data["relations"]:
            relations_by_family[relation["family_id"]].append(relation)
        for family in data["families"]:
            fid = family["family_id"]
            self.assertEqual(len(variants_by_family[fid]), 8)
            self.assertEqual(len(relations_by_family[fid]), 7)
            self.assertEqual(len({v["variant_type"] for v in variants_by_family[fid]}), 8)
            self.assertEqual(len({r["relation_type"] for r in relations_by_family[fid]}), 7)

    def test_variants_are_surgical_not_multi_fact_oracles(self):
        data = load_dataset(ROOT / "data" / "clinmap_voi_v0")
        for variant in data["variants"]:
            self.assertEqual(len(variant["changed_facts"]), 1, variant["variant_id"])
            self.assertTrue(variant["expected_safe_behavior_delta"])
            self.assertTrue(variant["disallowed_generic_response"])

    def test_relation_direction_mix_prevents_refer_everything_eval(self):
        data = load_dataset(ROOT / "data" / "clinmap_voi_v0")
        directions = Counter(r["expected_direction"] for r in data["relations"])
        self.assertEqual(directions["increase"], 200)
        self.assertEqual(directions["invariant"], 80)
        moves = Counter(v["optimal_model_move"] for v in data["variants"])
        self.assertGreaterEqual(moves["general_information_with_boundary"], 80)
        self.assertGreaterEqual(moves["ask_targeted_context_before_guidance"], 80)
        self.assertEqual(moves["recommend_urgent_assessment"], 40)

    def test_schema_file_exists_and_defines_relation(self):
        schema_path = ROOT / "schemas" / "clinmap_voi_v0_schemas.json"
        self.assertTrue(schema_path.exists())
        schema = json.loads(schema_path.read_text())
        self.assertIn("metamorphic_relation", schema["schemas"])
        self.assertIn("case_variant", schema["schemas"])


if __name__ == "__main__":
    unittest.main()

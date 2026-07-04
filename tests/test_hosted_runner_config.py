import json
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from clinmap_voi.common import read_jsonl
from model_runs.run_hosted_clinmap_voi import load_config, selected_models


def args(**overrides):
    base = {
        "providers": "",
        "models": "",
        "skip_models": "",
        "include_supplementary": False,
        "include_disabled": False,
    }
    base.update(overrides)
    return SimpleNamespace(**base)


class HostedRunnerConfigTests(unittest.TestCase):
    def test_config_has_expected_model_count_and_no_keys(self):
        config = load_config(ROOT / "model_runs" / "hosted_models_clinmap_voi_v0.json")
        self.assertEqual(len(config["models"]), 19)
        text = json.dumps(config).lower()
        self.assertNotIn("sk-", text)
        self.assertIn("groq_api_key", text)
        self.assertIn("cerebras_api_key", text)
        self.assertIn("mistral_api_key", text)
        self.assertIn("gemini_api_key", text)
        self.assertIn("nvidia_api_key", text)

    def test_default_selected_models_are_core_12_only(self):
        config = load_config(ROOT / "model_runs" / "hosted_models_clinmap_voi_v0.json")
        models = selected_models(config, args())
        self.assertEqual(len(models), 12)
        self.assertNotIn("google", {m["provider"] for m in models})
        self.assertNotIn("nvidia", {m["provider"] for m in models})

    def test_include_supplementary_adds_google_and_configured_nvidia_primary(self):
        config = load_config(ROOT / "model_runs" / "hosted_models_clinmap_voi_v0.json")
        with patch.dict(os.environ, {}, clear=True):
            models = selected_models(config, args(include_supplementary=True))
        self.assertEqual(len(models), 19)
        providers = {m["provider"] for m in models}
        self.assertIn("google", providers)
        self.assertIn("nvidia", providers)
        self.assertIn("nvidia/nemotron-3-ultra-550b-a55b", {m["model_id"] for m in models})
        self.assertIn("z-ai/glm-5.2", {m["model_id"] for m in models})
        self.assertIn("deepseek-ai/deepseek-v4-pro", {m["model_id"] for m in models})
        self.assertIn("meta/llama-3.3-70b-instruct", {m["model_id"] for m in models})

    def test_nvidia_supplementary_models_selected(self):
        config = load_config(ROOT / "model_runs" / "hosted_models_clinmap_voi_v0.json")
        with patch.dict(os.environ, {}, clear=True):
            models = selected_models(config, args(providers="nvidia", include_supplementary=True))
        self.assertEqual(len(models), 5)
        self.assertEqual({m["model_id"] for m in models}, {"nvidia/nemotron-3-ultra-550b-a55b", "nvidia/nemotron-3-super-120b-a12b", "z-ai/glm-5.2", "deepseek-ai/deepseek-v4-pro", "meta/llama-3.3-70b-instruct"})

    def test_config_model_aliases_are_unique(self):
        config = load_config(ROOT / "model_runs" / "hosted_models_clinmap_voi_v0.json")
        aliases = [m["alias"] for m in config["models"]]
        self.assertEqual(len(aliases), len(set(aliases)))

    def test_prompt_pack_matches_320_prompts(self):
        prompts = read_jsonl(ROOT / "data" / "clinmap_voi_v0" / "model_prompt_pack.jsonl")
        self.assertEqual(len(prompts), 320)

    def test_model_ids_are_provider_qualified_where_needed(self):
        config = load_config(ROOT / "model_runs" / "hosted_models_clinmap_voi_v0.json")
        groq_models = [m["model_id"] for m in config["models"] if m["provider"] == "groq"]
        self.assertIn("qwen/qwen3.6-27b", groq_models)
        self.assertIn("openai/gpt-oss-120b", groq_models)
        cerebras_models = [m["model_id"] for m in config["models"] if m["provider"] == "cerebras"]
        self.assertIn("zai-glm-4.7", cerebras_models)
        mistral_models = [m["model_id"] for m in config["models"] if m["provider"] == "mistral"]
        self.assertIn("mistral-large-2512", mistral_models)
        google_models = [m["model_id"] for m in config["models"] if m["provider"] == "google"]
        self.assertIn("gemini-3.5-flash", google_models)


if __name__ == "__main__":
    unittest.main()

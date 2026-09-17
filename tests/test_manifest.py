import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_manifest", ROOT / "scripts" / "validate_manifest.py")
validate_manifest = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_manifest)


class ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = json.loads((ROOT / "config" / "powerbi-project.template.json").read_text(encoding="utf-8"))

    def configured(self):
        manifest = copy.deepcopy(self.template)
        manifest["project"]["domain"] = "Finance"
        manifest["project"]["ownerTeam"] = "Analytics"
        manifest["connections"][0]["kind"] = "sql-server"
        manifest["connections"][0]["location"] = "server/database"
        return manifest

    def test_valid_local_model(self):
        self.assertEqual(validate_manifest.validate(self.configured()), [])

    def test_remote_model_requires_live_connection(self):
        manifest = self.configured()
        manifest["artifacts"]["semanticModel"]["kind"] = "remote"
        errors = validate_manifest.validate(manifest)
        self.assertTrue(any("remote semantic model" in error for error in errors))

    def test_duplicate_report_names_fail(self):
        manifest = self.configured()
        manifest["artifacts"]["reports"].append(copy.deepcopy(manifest["artifacts"]["reports"][0]))
        errors = validate_manifest.validate(manifest)
        self.assertTrue(any("Duplicate report name" in error for error in errors))

    def test_secret_fields_fail(self):
        manifest = self.configured()
        manifest["connections"][0]["password"] = "do-not-store-this"
        errors = validate_manifest.validate(manifest)
        self.assertTrue(any("forbidden secret fields" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

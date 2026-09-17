import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_salesdashboard", ROOT / "scripts" / "validate_salesdashboard.py"
)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


class ProjectTests(unittest.TestCase):
    def test_absolute_path_detection(self):
        self.assertTrue(validator.is_absolute_path(r"C:\PowerBI\data\sales.csv"))
        self.assertTrue(validator.is_absolute_path("/workspace/data/sales.csv"))
        self.assertFalse(validator.is_absolute_path("data/sales.csv"))

    def test_complete_project_contract(self):
        self.assertEqual(validator.main(), 0)


if __name__ == "__main__":
    unittest.main()

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("validate_project", ROOT / "scripts" / "validate_project.py")
validate_project = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_project)


class PathTests(unittest.TestCase):
    def test_windows_path(self):
        self.assertTrue(validate_project.is_absolute_path(r"C:\data\source.csv"))

    def test_unc_path(self):
        self.assertTrue(validate_project.is_absolute_path(r"\\server\share\source.csv"))

    def test_posix_path(self):
        self.assertTrue(validate_project.is_absolute_path("/data/source.csv"))

    def test_relative_path(self):
        self.assertFalse(validate_project.is_absolute_path("data/source.csv"))


if __name__ == "__main__":
    unittest.main()

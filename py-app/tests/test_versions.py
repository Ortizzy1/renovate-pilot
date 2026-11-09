import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pilot_py.versions import is_compatible, newest  # noqa: E402


class SmokeTest(unittest.TestCase):
    def test_inside_specifier(self):
        self.assertTrue(is_compatible("1.4.2", ">=1.2,<2"))

    def test_outside_specifier(self):
        self.assertFalse(is_compatible("2.0.0", ">=1.2,<2"))

    def test_newest_ignores_junk(self):
        self.assertEqual(newest(["1.0", "junk", "1.10", "1.9.9"]), "1.10")
        self.assertIsNone(newest([]))


if __name__ == "__main__":
    unittest.main()

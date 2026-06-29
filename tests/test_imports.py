import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ImportTests(unittest.TestCase):
    def test_package_import_from_outside_project_root(self):
        repo_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-c", "import pdga_scraper; print(pdga_scraper.__file__)"],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                env=os.environ.copy(),
                check=False,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"Import failed from outside the repo root.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
            )
            self.assertIn("pdga_scraper", result.stdout)


if __name__ == "__main__":
    unittest.main()

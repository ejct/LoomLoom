import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install.py"
VERSION = "v0.3.0-alpha.2"


class InstallerE2ETests(unittest.TestCase):
    def test_tagged_source_installs_exact_pin_and_skill(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            source = temp / "source"
            project = temp / "project"
            project.mkdir()

            subprocess.run(["git", "clone", "--quiet", str(ROOT), str(source)], check=True)
            subprocess.run(["git", "-C", str(source), "tag", VERSION], check=True)
            expected = subprocess.check_output(
                ["git", "-C", str(source), "rev-parse", VERSION],
                text=True,
            ).strip()

            env = os.environ.copy()
            env["LOOMLOOM_GIT_URL"] = source.as_uri()
            env["LOOMLOOM_VERSION"] = VERSION
            env["LOOMLOOM_REPOSITORY"] = "ejct/LoomLoom"

            completed = subprocess.run(
                [sys.executable, str(INSTALLER), str(project)],
                env=env,
                text=True,
                capture_output=True,
                check=True,
            )

            lock = json.loads((project / ".loomloom/loomloom.lock").read_text(encoding="utf-8"))
            self.assertEqual(lock["commit"], expected)
            self.assertEqual(lock["release"], VERSION)
            self.assertEqual(lock["distribution"], "github_release")
            self.assertTrue((project / ".agents/skills/loomloom-bootstrap/SKILL.md").is_file())
            self.assertIn(f"Pinned: ejct/LoomLoom@{expected}", completed.stdout)


if __name__ == "__main__":
    unittest.main()

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "init_project.py"
spec = importlib.util.spec_from_file_location("init_project", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InitProjectTests(unittest.TestCase):
    COMMIT = "0123456789abcdef0123456789abcdef01234567"

    def setUp(self):
        self.source_tmp = tempfile.TemporaryDirectory()
        self.project_tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.source_tmp.cleanup)
        self.addCleanup(self.project_tmp.cleanup)
        self.source = Path(self.source_tmp.name)
        self.project = Path(self.project_tmp.name)
        skill = self.source / ".agents/skills/loomloom-bootstrap"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text("skill\n", encoding="utf-8")
        (skill / "references/BOOTSTRAP.md").write_text("bootstrap\n", encoding="utf-8")

    def test_install_and_idempotency(self):
        args = dict(commit=self.COMMIT, release="v0.3.0-alpha.2")
        first = module.initialize_project(self.project, self.source, **args)
        second = module.initialize_project(self.project, self.source, **args)
        lock = json.loads((self.project / ".loomloom/loomloom.lock").read_text())
        self.assertEqual(lock["commit"], self.COMMIT)
        self.assertEqual(lock["distribution"], "github_release")
        self.assertEqual(first["skill"], "installed")
        self.assertEqual(second["skill"], "unchanged")

    def test_existing_other_pin_is_rejected(self):
        lock_path = self.project / ".loomloom/loomloom.lock"
        lock_path.parent.mkdir(parents=True)
        lock_path.write_text(json.dumps({
            "schema_version": 1,
            "repository": "ejct/LoomLoom",
            "commit": "89abcdef0123456789abcdef0123456789abcdef",
            "distribution": "github_release",
            "release": "v0.3.0-alpha.1"
        }), encoding="utf-8")
        with self.assertRaises(module.InitError):
            module.initialize_project(self.project, self.source, commit=self.COMMIT, release="v0.3.0-alpha.2")
        self.assertFalse((self.project / ".agents/skills/loomloom-bootstrap").exists())

    def test_existing_different_skill_is_rejected(self):
        skill = self.project / ".agents/skills/loomloom-bootstrap"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("different\n", encoding="utf-8")
        with self.assertRaises(module.InitError):
            module.initialize_project(self.project, self.source, commit=self.COMMIT, release="v0.3.0-alpha.2")
        self.assertFalse((self.project / ".loomloom/loomloom.lock").exists())


if __name__ == "__main__":
    unittest.main()

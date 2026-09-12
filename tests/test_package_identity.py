import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "package_identity.py"
spec = importlib.util.spec_from_file_location("package_identity", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PackageIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        module.ROOT = self.root
        module.MANIFEST = self.root / "loomloom-package.json"
        (self.root / "README.md").write_text("alpha\n", encoding="utf-8")
        (self.root / "nested").mkdir()
        (self.root / "nested" / "data.txt").write_text("beta\n", encoding="utf-8")

    def quiet(self, fn):
        with redirect_stdout(StringIO()):
            return fn()

    def create_manifest(self):
        self.assertEqual(self.quiet(module.create), 0)
        self.assertTrue(module.MANIFEST.is_file())

    def test_create_then_verify_passes(self):
        self.create_manifest()
        self.assertEqual(self.quiet(module.verify), 0)

    def test_changed_file_fails_verification(self):
        self.create_manifest()
        (self.root / "README.md").write_text("changed\n", encoding="utf-8")
        self.assertEqual(self.quiet(module.verify), 1)

    def test_added_file_fails_verification(self):
        self.create_manifest()
        (self.root / "new.txt").write_text("new\n", encoding="utf-8")
        self.assertEqual(self.quiet(module.verify), 1)

    def test_deleted_file_fails_verification(self):
        self.create_manifest()
        (self.root / "nested" / "data.txt").unlink()
        self.assertEqual(self.quiet(module.verify), 1)

    def test_source_commit_is_descriptive_not_content_binding(self):
        self.create_manifest()
        manifest = json.loads(module.MANIFEST.read_text(encoding="utf-8"))
        manifest["source_commit"] = "f" * 40
        module.MANIFEST.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        self.assertEqual(self.quiet(module.verify), 0)


if __name__ == "__main__":
    unittest.main()

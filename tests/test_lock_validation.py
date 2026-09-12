import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_loomloom_pin.py"
spec = importlib.util.spec_from_file_location("validate_loomloom_pin", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class LockValidationTests(unittest.TestCase):
    def write_raw(self, text: str):
        temp = tempfile.TemporaryDirectory()
        path = Path(temp.name) / "loomloom.lock"
        path.write_text(text, encoding="utf-8")
        self.addCleanup(temp.cleanup)
        return path

    def write_lock(self, payload):
        return self.write_raw(json.dumps(payload))

    def valid_payload(self):
        return {
            "schema_version": 1,
            "repository": "owner/LoomLoom",
            "commit": "0123456789abcdef0123456789abcdef01234567",
            "distribution": "git_commit",
            "release": None,
        }

    def test_exact_commit_validates_to_pinned_identity(self):
        payload = self.valid_payload()
        result = module.validate_lock(self.write_lock(payload))
        self.assertEqual(
            result["pinned_identity"],
            f'{payload["repository"]}@{payload["commit"]}',
        )

    def test_short_commit_is_rejected(self):
        payload = self.valid_payload()
        payload["commit"] = "abcdef1"
        with self.assertRaises(module.LockError):
            module.validate_lock(self.write_lock(payload))

    def test_branch_name_is_rejected_as_commit(self):
        payload = self.valid_payload()
        payload["commit"] = "main"
        with self.assertRaises(module.LockError):
            module.validate_lock(self.write_lock(payload))

    def test_unknown_fields_are_rejected(self):
        payload = self.valid_payload()
        payload["latest"] = True
        with self.assertRaises(module.LockError):
            module.validate_lock(self.write_lock(payload))

    def test_invalid_json_is_rejected(self):
        with self.assertRaises(module.LockError):
            module.validate_lock(self.write_raw("{not-json"))

    def test_invalid_repository_shape_is_rejected(self):
        payload = self.valid_payload()
        payload["repository"] = "LoomLoom"
        with self.assertRaises(module.LockError):
            module.validate_lock(self.write_lock(payload))

    def test_invalid_distribution_is_rejected(self):
        payload = self.valid_payload()
        payload["distribution"] = "latest"
        with self.assertRaises(module.LockError):
            module.validate_lock(self.write_lock(payload))

    def test_release_is_descriptive_and_does_not_override_commit(self):
        payload = self.valid_payload()
        payload["distribution"] = "github_release"
        payload["release"] = "v999"
        result = module.validate_lock(self.write_lock(payload))
        self.assertEqual(
            result["pinned_identity"],
            f'{payload["repository"]}@{payload["commit"]}',
        )


if __name__ == "__main__":
    unittest.main()

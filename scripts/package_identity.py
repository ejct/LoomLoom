#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "loomloom-package.json"
EXCLUDED_DIRS = {".git", "__pycache__"}
EXCLUDED_FILES = {"loomloom-package.json"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files() -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if rel.as_posix() in EXCLUDED_FILES:
            continue
        files[rel.as_posix()] = sha256_file(path)
    return files


def content_digest(files: dict[str, str]) -> str:
    payload = json.dumps(files, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def source_commit() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return None
    return out if len(out) == 40 and all(c in "0123456789abcdef" for c in out.lower()) else None


def create() -> int:
    files = collect_files()
    manifest = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "content_digest": content_digest(files),
        "files": files,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(MANIFEST)
    print(manifest["content_digest"])
    return 0


def verify() -> int:
    if not MANIFEST.is_file():
        print("FAIL: loomloom-package.json missing")
        return 1
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAIL: invalid manifest JSON: {e}")
        return 1

    expected_files = manifest.get("files")
    expected_digest = manifest.get("content_digest")
    if not isinstance(expected_files, dict) or not isinstance(expected_digest, str):
        print("FAIL: manifest missing files/content_digest")
        return 1

    actual_files = collect_files()
    actual_digest = content_digest(actual_files)
    if actual_files != expected_files:
        expected_keys = set(expected_files)
        actual_keys = set(actual_files)
        for path in sorted(expected_keys - actual_keys):
            print(f"MISSING: {path}")
        for path in sorted(actual_keys - expected_keys):
            print(f"UNEXPECTED: {path}")
        for path in sorted(expected_keys & actual_keys):
            if expected_files[path] != actual_files[path]:
                print(f"CHANGED: {path}")
        print("FAIL: package file identity mismatch")
        return 1
    if actual_digest != expected_digest:
        print("FAIL: content_digest mismatch")
        return 1

    print("PASS")
    print(actual_digest)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["create", "verify"])
    args = parser.parse_args()
    return create() if args.command == "create" else verify()


if __name__ == "__main__":
    sys.exit(main())

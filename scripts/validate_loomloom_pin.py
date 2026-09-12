#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REPO_RE = re.compile(r"^[^/\s]+/[^/\s]+$")
ALLOWED_DISTRIBUTIONS = {"git_commit", "github_release"}
ALLOWED_KEYS = {"schema_version", "repository", "commit", "distribution", "release"}


class LockError(ValueError):
    pass


def validate_lock(path: Path) -> dict:
    """Validate and normalize a LoomLoom lock.

    This function does not contact a repository and therefore does not prove
    that the pinned commit exists or is accessible. Repository availability is
    a consuming-runtime/adapter responsibility.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise LockError(f"invalid lock JSON: {e}") from e

    if not isinstance(data, dict):
        raise LockError("lock must be a JSON object")

    unknown = set(data) - ALLOWED_KEYS
    if unknown:
        raise LockError(f"unknown lock fields: {', '.join(sorted(unknown))}")

    if data.get("schema_version") != 1:
        raise LockError("schema_version must be 1")

    repository = data.get("repository")
    commit = data.get("commit")
    distribution = data.get("distribution")
    release = data.get("release")

    if not isinstance(repository, str) or not REPO_RE.fullmatch(repository):
        raise LockError("repository must be owner/name")
    if not isinstance(commit, str) or not COMMIT_RE.fullmatch(commit):
        raise LockError("commit must be an exact 40-character lowercase hex Git SHA")
    if distribution not in ALLOWED_DISTRIBUTIONS:
        raise LockError("distribution must be git_commit or github_release")
    if release is not None and not isinstance(release, str):
        raise LockError("release must be string or null")

    return {
        "schema_version": 1,
        "repository": repository,
        "commit": commit,
        "distribution": distribution,
        "release": release,
        "pinned_identity": f"{repository}@{commit}",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate and normalize a LoomLoom project lock. "
            "This does not verify repository/commit availability."
        )
    )
    parser.add_argument("lock", nargs="?", default=".loomloom/loomloom.lock")
    args = parser.parse_args()

    try:
        validated = validate_lock(Path(args.lock))
    except LockError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 2

    print(json.dumps(validated, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

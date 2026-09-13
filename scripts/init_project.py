#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

DEFAULT_REPOSITORY = "ejct/LoomLoom"
LOCK_REL = Path(".loomloom/loomloom.lock")
SKILL_REL = Path(".agents/skills/loomloom-bootstrap")


class InitError(RuntimeError):
    pass


def _exact_commit(value: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value or ""):
        raise InitError("commit must be an exact 40-character lowercase Git SHA")
    return value


def _load_lock(path: Path):
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InitError(f"existing LoomLoom lock is invalid JSON: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise InitError(f"existing LoomLoom lock must be a JSON object: {path}")
    return payload


def _tree_snapshot(root: Path):
    if not root.is_dir():
        return None
    snapshot = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        snapshot[path.relative_to(root).as_posix()] = path.read_bytes()
    return snapshot


def _desired_lock(repository: str, commit: str, release: str | None):
    payload = {
        "schema_version": 1,
        "repository": repository,
        "commit": _exact_commit(commit),
        "distribution": "github_release" if release else "git_commit",
    }
    if release:
        payload["release"] = release
    return payload


def initialize_project(
    project: Path,
    source: Path,
    repository: str = DEFAULT_REPOSITORY,
    commit: str = "",
    release: str | None = None,
):
    project = project.resolve()
    source = source.resolve()
    if not project.is_dir():
        raise InitError(f"project directory does not exist: {project}")
    if not re.fullmatch(r"[^/\s]+/[^/\s]+", repository or ""):
        raise InitError("repository must use owner/name form")

    desired_lock = _desired_lock(repository, commit, release)
    source_skill = source / SKILL_REL
    if not source_skill.is_dir():
        raise InitError(f"source distribution is missing {SKILL_REL}")

    lock_path = project / LOCK_REL
    skill_path = project / SKILL_REL

    existing_lock = _load_lock(lock_path) if lock_path.exists() else None
    if existing_lock is not None:
        existing_repo = existing_lock.get("repository")
        existing_commit = existing_lock.get("commit")
        if existing_repo != repository or existing_commit != commit:
            raise InitError(
                "project already has a different LoomLoom pin; refusing a silent upgrade "
                f"({existing_repo}@{existing_commit} != {repository}@{commit})"
            )

    source_snapshot = _tree_snapshot(source_skill)
    dest_snapshot = _tree_snapshot(skill_path)
    if dest_snapshot is not None and dest_snapshot != source_snapshot:
        raise InitError(
            f"{SKILL_REL} already exists and differs from this LoomLoom release; "
            "refusing to overwrite local or differently-versioned skill files"
        )

    lock_state = "unchanged"
    if existing_lock != desired_lock:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path.write_text(json.dumps(desired_lock, indent=2) + "\n", encoding="utf-8")
        lock_state = "created" if existing_lock is None else "updated"

    skill_state = "unchanged"
    if dest_snapshot is None:
        skill_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_skill, skill_path)
        skill_state = "installed"

    return {
        "project": str(project),
        "pinned_identity": f"{repository}@{commit}",
        "release": release,
        "lock": lock_state,
        "skill": skill_state,
    }


def build_parser():
    parser = argparse.ArgumentParser(description="Install a pinned LoomLoom Bootstrap skill and lock into an existing project.")
    parser.add_argument("--project", default=".", help="target project directory")
    parser.add_argument("--source", required=True, help="LoomLoom release checkout")
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY, help="LoomLoom repository in owner/name form")
    parser.add_argument("--commit", required=True, help="exact 40-character release commit")
    parser.add_argument("--release", help="release/tag provenance")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        result = initialize_project(Path(args.project), Path(args.source), args.repository, args.commit, args.release)
    except InitError as exc:
        print(f"LoomLoom setup failed: {exc}", file=sys.stderr)
        return 2

    release = f" ({result['release']})" if result["release"] else ""
    print(f"LoomLoom ready{release}.")
    print(f"Pinned: {result['pinned_identity']}")
    print(f"Lock: {LOCK_REL} [{result['lock']}]")
    print(f"Skill: {SKILL_REL} [{result['skill']}]")
    print("Next: ask your coding agent: 'Use LoomLoom for this task: <your task>.'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

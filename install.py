#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_VERSION = "v0.3.0-alpha.2"
DEFAULT_REPOSITORY = "ejct/LoomLoom"


def run(command, **kwargs):
    try:
        return subprocess.run(command, check=True, text=True, **kwargs)
    except FileNotFoundError as exc:
        raise RuntimeError(f"required command not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"command failed ({exc.returncode}): {' '.join(command)}") from exc


def main():
    version = os.environ.get("LOOMLOOM_VERSION", DEFAULT_VERSION)
    repository = os.environ.get("LOOMLOOM_REPOSITORY", DEFAULT_REPOSITORY)
    project = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    repo_url = os.environ.get("LOOMLOOM_GIT_URL", f"https://github.com/{repository}.git")

    if not project.is_dir():
        raise RuntimeError(f"project directory does not exist: {project}")

    with tempfile.TemporaryDirectory(prefix="loomloom-") as temp_dir:
        checkout = Path(temp_dir) / "LoomLoom"
        run(["git", "clone", "--quiet", "--depth", "1", "--branch", version, repo_url, str(checkout)])

        tag_check = subprocess.run(
            ["git", "-C", str(checkout), "show-ref", "--verify", "--quiet", f"refs/tags/{version}"],
            text=True,
        )
        if tag_check.returncode != 0:
            raise RuntimeError(f"{version} is not an immutable release tag")

        commit = subprocess.check_output(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"],
            text=True,
        ).strip()

        run([
            sys.executable,
            str(checkout / "scripts/init_project.py"),
            "--project", str(project),
            "--source", str(checkout),
            "--repository", repository,
            "--commit", commit,
            "--release", version,
        ])


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(f"LoomLoom setup failed: {exc}", file=sys.stderr)
        raise SystemExit(2)

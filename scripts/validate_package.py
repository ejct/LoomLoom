#!/usr/bin/env python3
from pathlib import Path
import re, sys, json

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md",
    "START_HERE.md",
    "AGENTS.md",
    "loomloom.yaml",
    "install.py",
    "bootstrap/BOOTSTRAP.md",
    "bootstrap/CONTEXT_RECEIPT.md",
    "bootstrap/ROUTING.md",
    "bootstrap/PINNING.md",
    "bootstrap/PACKAGE_IDENTITY.md",
    "schemas/loomloom-lock.schema.json",
    "fixtures/loomloom.lock.example",
    "scripts/init_project.py",
    "scripts/validate_loomloom_pin.py",
    "scripts/package_identity.py",
    "tests/test_init_project.py",
    "tests/test_installer_e2e.py",
    "tests/test_lock_validation.py",
    "tests/test_package_identity.py",
    ".agents/skills/loomloom-bootstrap/SKILL.md",
    ".agents/skills/loomloom-bootstrap/references/BOOTSTRAP.md",
    ".agents/skills/loomloom-bootstrap/references/CONTEXT_RECEIPT.md",
    ".agents/skills/loomloom-bootstrap/references/ROUTING.md",
    ".agents/skills/loomloom-bootstrap/references/PINNING.md",
    ".agents/skills/loomloom-bootstrap/references/PACKAGE_IDENTITY.md",
    "policy/agent-operating-behavior.md",
    "profiles/browser-extension-development.md",
    "fixtures/bootstrap-cases.json",
]

errors = []
for rel in required:
    if not (ROOT / rel).is_file():
        errors.append(f"missing: {rel}")

legacy_paths = [
    "skills/loomloom-bootstrap",
    "scripts/resolve_loomloom_pin.py",
    "tests/test_lock_resolution.py",
]
for rel in legacy_paths:
    if (ROOT / rel).exists():
        errors.append(f"legacy path still present: {rel}")

skill = ROOT / ".agents/skills/loomloom-bootstrap/SKILL.md"
if skill.is_file():
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md: missing opening YAML frontmatter")
    m = re.match(r"---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        errors.append("SKILL.md: malformed YAML frontmatter delimiters")
    else:
        fm = m.group(1)
        name = re.search(r"^name:\s*(.+)$", fm, flags=re.M)
        desc = re.search(r"^description:\s*(.+)$", fm, flags=re.M)
        if not name:
            errors.append("SKILL.md: missing name")
        else:
            value = name.group(1).strip()
            if value != "loomloom-bootstrap":
                errors.append(f"SKILL.md: unexpected name {value!r}")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
                errors.append("SKILL.md: name violates Agent Skills naming rule")
        if not desc or not desc.group(1).strip():
            errors.append("SKILL.md: missing description")

mirror_pairs = [
    ("bootstrap/BOOTSTRAP.md", ".agents/skills/loomloom-bootstrap/references/BOOTSTRAP.md"),
    ("bootstrap/CONTEXT_RECEIPT.md", ".agents/skills/loomloom-bootstrap/references/CONTEXT_RECEIPT.md"),
    ("bootstrap/ROUTING.md", ".agents/skills/loomloom-bootstrap/references/ROUTING.md"),
    ("bootstrap/PINNING.md", ".agents/skills/loomloom-bootstrap/references/PINNING.md"),
    ("bootstrap/PACKAGE_IDENTITY.md", ".agents/skills/loomloom-bootstrap/references/PACKAGE_IDENTITY.md"),
]
for a, b in mirror_pairs:
    pa, pb = ROOT / a, ROOT / b
    if pa.is_file() and pb.is_file() and pa.read_bytes() != pb.read_bytes():
        errors.append(f"portable skill mirror drift: {a} != {b}")

fixtures = ROOT / "fixtures/bootstrap-cases.json"
if fixtures.is_file():
    try:
        data = json.loads(fixtures.read_text(encoding="utf-8"))
        if len(data.get("cases", [])) < 5:
            errors.append("fixtures: expected at least 5 bootstrap cases")
    except Exception as e:
        errors.append(f"fixtures JSON invalid: {e}")

lock_schema = ROOT / "schemas/loomloom-lock.schema.json"
if lock_schema.is_file():
    try:
        schema = json.loads(lock_schema.read_text(encoding="utf-8"))
        required_lock = set(schema.get("required", []))
        if required_lock != {"schema_version", "repository", "commit", "distribution"}:
            errors.append("lock schema: unexpected required field set")
    except Exception as e:
        errors.append(f"lock schema JSON invalid: {e}")

lock_example = ROOT / "fixtures/loomloom.lock.example"
if lock_example.is_file():
    try:
        lock = json.loads(lock_example.read_text(encoding="utf-8"))
        if lock.get("schema_version") != 1:
            errors.append("lock example: schema_version must be 1")
        if not re.fullmatch(r"[^/\s]+/[^/\s]+", str(lock.get("repository", ""))):
            errors.append("lock example: repository must be owner/name")
        if not re.fullmatch(r"[0-9a-f]{40}", str(lock.get("commit", ""))):
            errors.append("lock example: commit must be exact 40-char lowercase hex SHA")
        if lock.get("distribution") not in {"git_commit", "github_release"}:
            errors.append("lock example: invalid distribution")
    except Exception as e:
        errors.append(f"lock example JSON invalid: {e}")

metadata = ROOT / "loomloom.yaml"
installer = ROOT / "install.py"
if metadata.is_file() and installer.is_file():
    version_match = re.search(r"^version:\s*([^\s]+)$", metadata.read_text(encoding="utf-8"), flags=re.M)
    installer_match = re.search(r'^DEFAULT_VERSION\s*=\s*"v([^"]+)"$', installer.read_text(encoding="utf-8"), flags=re.M)
    if not version_match:
        errors.append("loomloom.yaml: missing distribution version")
    elif not installer_match:
        errors.append("install.py: missing DEFAULT_VERSION")
    elif version_match.group(1) != installer_match.group(1):
        errors.append("distribution metadata / installer version drift")

if errors:
    print("FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("PASS")
print("LoomLoom distribution package structure is internally valid.")

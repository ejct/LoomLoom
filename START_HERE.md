# START HERE — LoomLoom

Use this file to enter LoomLoom without loading project history that is not material to the current task.

## 1. Determine operating mode

### Consumer project

You are working in a project that uses a released LoomLoom distribution.

1. Look for `.loomloom/loomloom.lock`.
2. If present, validate and normalize it with `scripts/validate_loomloom_pin.py` when repository tooling is available; see `bootstrap/PINNING.md`.
3. Resolve the exact pinned `repository@commit` through the current repository/runtime adapter.
4. Do **not** silently upgrade to a newer release or branch HEAD.
5. Record the exact commit actually used in the Context Receipt.
6. Load only LoomLoom material relevant to the task.

For a tagged LoomLoom release, the exact tag/commit and repository contents at that tag are the public distribution authority for that version.

### LoomLoom development

You are changing or reviewing LoomLoom itself.

1. Identify whether the subject is a released tag, a release candidate branch, or an unreleased development branch.
2. For a released version, treat the exact tagged repository contents as the public distribution authority.
3. For unreleased LoomLoom development, use the explicitly supplied project-governance/status sources when available. Do not infer acceptance from repository HEAD, recency, or location.
4. Read only the accepted decisions, specifications, experiments, or evidence material relevant to the requested change.
5. Treat research and historical material as non-authoritative unless the task explicitly requires it.

A private governance workspace may prepare future releases, but it is not required to consume an existing public release and cannot silently change the meaning of an already tagged subject.

### Portable snapshot

No Git repository or release tag is available.

Use the explicitly supplied LoomLoom package/capsule as a frozen snapshot. If `loomloom-package.json` is present, verify package identity using `bootstrap/PACKAGE_IDENTITY.md` / `scripts/package_identity.py` when available.

Package verification proves content identity only. It does not make a snapshot current, accepted, or equivalent to a tagged release.

## 2. Source classes

- **RELEASED DISTRIBUTION** — accepted public LoomLoom subject at an immutable version/tag/commit.
- **CANON / ACCEPTED DECISION** — authoritative semantic or project-governance material for its stated scope.
- **CANDIDATE** — proposed implementation/distribution subject; not accepted by existence.
- **EXPERIMENT** — may govern only its authorized experiment.
- **RESEARCH** — advisory evidence; no authority by existence.
- **ARCHIVE / SUPERSEDED** — historical only unless explicitly requested.

Filename recency, branch HEAD, CI success, merge state, or tool capability do not create authority.

## 3. Agent operating behavior

Within the resolved Authority Envelope:

- be proactive on safe, reversible, in-scope next steps;
- use tools, automation, alternate runtimes, test harnesses, and lower-interference execution surfaces before shifting recurring work to a human;
- diagnose blocked methods and try reasonable alternatives;
- after changes, close the verification loop when possible;
- match claims to evidence fidelity;
- never treat proactivity as authority escalation.

See `policy/agent-operating-behavior.md` when material.

## 4. Task-specific loading

Load the smallest context sufficient for the task.

Do not load unrelated research or historical material “just in case.”
Do not import proposals as current decisions.

For browser-extension development, load `profiles/browser-extension-development.md` before accepting a recurring human-gated browser test loop.

See `bootstrap/ROUTING.md`.

## 5. Before substantive authority-sensitive work

Emit a concise **LoomLoom Context Receipt** using `bootstrap/CONTEXT_RECEIPT.md`.

If material sources conflict, stop the blocked authority-sensitive action and report `NEEDS_DECISION` rather than silently choosing a source.

## 6. Core invariants

- No capability creates authority by itself.
- Evidence always refers to an exactly identified subject.
- Producer self-report is not independent evidence.
- No success signal automatically raises the authority state of an artifact.
- A result cannot be treated as reproducible when its material execution context is unknown.
- Proactivity does not create authority.

For the full public Kernel specification, read `docs/DEVELOPMENT_KERNEL.md`.

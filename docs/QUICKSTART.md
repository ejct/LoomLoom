# LoomLoom Quickstart

Start from the root of an existing project. You do not need to create LoomLoom files by hand.

## 1. Set up LoomLoom

On macOS or Linux:

```sh
curl -fsSL https://raw.githubusercontent.com/ejct/LoomLoom/v0.3.0-alpha.2/install.py -o /tmp/loomloom-install.py && python3 /tmp/loomloom-install.py . && rm -f /tmp/loomloom-install.py
```

Setup uses the released tag, resolves its exact 40-character commit, and leaves these project-local surfaces:

```text
.loomloom/loomloom.lock
.agents/skills/loomloom-bootstrap/
```

It is deliberately fail-closed:

- an existing different LoomLoom pin is not silently replaced;
- an existing different Bootstrap skill is not overwritten;
- rerunning setup for the same exact release is idempotent.

If you prefer, hand the setup to your coding agent instead:

> Set up LoomLoom v0.3.0-alpha.2 from https://github.com/ejct/LoomLoom/tree/v0.3.0-alpha.2, using that release’s installer. Pin the exact tagged commit, then use LoomLoom for this task: **<your real task>**.

## 2. Give the agent the real task

If your runtime discovers repository Agent Skills automatically:

> Use LoomLoom for this task: **<your real task>**.

Otherwise tell it to read `.agents/skills/loomloom-bootstrap/SKILL.md` first.

Before consequential work, the agent should be able to report:

- exact LoomLoom identity: `ejct/LoomLoom@<40-char commit>`;
- project/task identity;
- material authority constraints;
- material sources it actually read;
- evidence expectations when they affect the task;
- the next bounded action.

This is the LoomLoom Context Receipt. It is a compact receipt for material execution context, not a transcript and not a universal evidence log.

`READY` means work can proceed.
`INCOMPLETE` means useful bounded work may continue with limited claims.
`NEEDS_DECISION` means a material authority conflict blocks the requested authority-sensitive action.

## 3. Run a real task

Good first tasks are work you would already trust to a coding agent but where a wrong scope or weak success claim would cost time: a bug fix, retained feature, migration, multi-file refactor, browser-extension repair, or work that will cross sessions.

The practical loop is:

`intent/contract → authorized implementation → exact candidate → observations/evidence → evaluation → explicit acceptance when required → reconciliation`

LoomLoom should reuse the project’s own issue/spec/test/CI/documentation surfaces when they already express the needed truth. It should not manufacture extra files merely to materialize every control concept.

## 4. Expect evidence proportional to the claim

Examples:

- a unit test does not prove production behavior it did not exercise;
- a page probe does not prove an unpacked browser extension works;
- an agent saying “tests pass” is a claim until tied to an observed exact subject;
- CI success does not accept a candidate;
- a merge does not prove post-integration correctness.

Verification evidence normally stays in project-native surfaces such as tests, CI results, build output, version-control state, issue/spec records, or existing evidence documentation.

## 5. Let continuation state stay small

A Context Receipt may exist only in the active session when nobody later needs it. When durable continuation or review materially depends on it, reuse an adequate project-native current-state/documentation owner if one exists; otherwise `.loomloom/context-receipt.yaml` is the fallback.

Do not create duplicate state just to satisfy LoomLoom.

## What setup actually pins

`.loomloom/loomloom.lock` records the exact LoomLoom source identity. Conceptually:

```json
{
  "schema_version": 1,
  "repository": "ejct/LoomLoom",
  "commit": "<exact 40-character release commit>",
  "distribution": "github_release",
  "release": "v0.3.0-alpha.2"
}
```

The commit is binding. The human-readable release name is provenance and never overrides the exact commit.

## Troubleshooting

### The project already has a different LoomLoom pin

Treat this as an explicit upgrade decision. Do not replace the lock automatically. Review compatibility, then change the project pin deliberately.

### The Bootstrap skill already exists and differs

Do not overwrite it blindly. Determine whether it is a local customization, another LoomLoom version, or unrelated project material.

### The runtime does not auto-discover Agent Skills

Tell the agent to read `.agents/skills/loomloom-bootstrap/SKILL.md` explicitly. The skill is the compact navigator; deeper LoomLoom sources are loaded only when they can materially affect the task or claim.

### The agent cannot access GitHub

Supply the exact tagged LoomLoom release/package through a permitted local or connected source. Preserve the same exact identity; do not substitute mutable branch HEAD.

## Upgrade explicitly

When a newer LoomLoom version exists, upgrading is a project change. Resolve the new exact release commit, replace the installed Bootstrap projection only with explicit intent, update the project lock, and re-evaluate material compatibility differences.

For deeper semantics, see `docs/DEVELOPMENT_KERNEL.md`. For versioning, see `VERSIONING.md`.

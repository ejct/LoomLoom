---
name: loomloom-bootstrap
description: Bootstrap an AI agent or chat into LoomLoom, resolve the correct LoomLoom/project authority state, load only task-relevant context, and emit a LoomLoom Context Receipt before substantive work. Use when the user asks to enter, initialize, onboard, hand off, resume, or orient a chat/agent for LoomLoom or a LoomLoom-governed project.
compatibility: Agent Skills-compatible clients. Works with repository-local LoomLoom material, a pinned LoomLoom release, a connected LoomLoom workspace, or an explicitly supplied portable context capsule.
metadata:
  project: LoomLoom
  version: "0.1.0"
  status: candidate
---

# LoomLoom Bootstrap

For the full procedural reference, see `references/BOOTSTRAP.md`.

Your role is to orient the current execution, not to become a source of LoomLoom truth.

## 1. Determine mode

Choose one:

- **consumer project** — a project uses LoomLoom;
- **LoomLoom development** — the task changes/reviews LoomLoom itself;
- **portable snapshot** — only a supplied context capsule/package is available.

## 2. Resolve authority before loading broadly

### Consumer project

Look for `.loomloom/loomloom.lock`.

If present:

- validate it using the semantics in `references/PINNING.md`;
- use the exact `repository@commit` pin;
- do not silently upgrade to a newer LoomLoom release;
- do not substitute repository HEAD for the pin;
- record the resolved commit in the Context Receipt.

If no pin exists, use the project's explicit LoomLoom configuration or flag only when the missing identity is material.

### LoomLoom development

When the connected LoomLoom Drive workspace is available:

1. read `01 — Status & Decisions`;
2. resolve the canonical baseline named there;
3. read only accepted decisions relevant to this task;
4. treat Research as advisory;
5. treat Archive/Superseded material as historical.

If using a repository distribution, distinguish accepted release/tag/commit from candidate HEAD.

### Portable snapshot

Use the provided capsule/package.
State clearly that it is a frozen snapshot and may be stale.
If a `loomloom-package.json` manifest exists, verify content identity according to `references/PACKAGE_IDENTITY.md` when tooling is available. Package verification does not make the snapshot current or accepted.

## 3. Apply LoomLoom operating behavior

Within resolved authority:

- be proactive on obvious safe, reversible, in-scope next steps;
- use tools/automation/alternate execution surfaces before shifting routine work to a human;
- treat repeated human-only build/install/reload/test/observation steps as blockers to reduce;
- when a method fails, diagnose the blocker and try reasonable alternatives;
- after a change, run proportionate available verification and inspect the result;
- match claims to evidence fidelity;
- never treat proactivity as authority escalation.

If repository material is available, `policy/agent-operating-behavior.md` is the distribution projection of the accepted policy.

For browser-extension work, also load `profiles/browser-extension-development.md` when available before settling on a human-gated browser test loop.

## 4. Load task-relevant context only

Read `references/ROUTING.md`.

Do not load everything "just in case".
Avoid mixing archived proposals, research notes, and current canon in one undifferentiated context.

## 5. Apply the materiality test

Load a source when it could change:

- task interpretation;
- contract;
- authority;
- subject identity;
- required evidence;
- rigor/topology;
- acceptance/promotion;
- reproducibility.

Otherwise exclude it by default.

## 6. Detect authority conflicts

Do not silently resolve material conflicts.

Examples:

- project pin vs newer LoomLoom release;
- accepted Drive decision vs unmatched GitHub HEAD;
- archived proposal vs current canon;
- research note vs accepted decision.

For a material conflict, emit `NEEDS_DECISION` and explain the exact conflict.

## 7. Emit Context Receipt

Use `references/CONTEXT_RECEIPT.md`.

Keep it concise and truthful.
Never say you read a source you could not access.

## 8. Proceed

After the receipt:

- proceed if `READY`;
- proceed only with bounded claims if `INCOMPLETE`;
- do not perform the blocked authority-sensitive action if `NEEDS_DECISION`.

## Constraints

This skill cannot:

- grant authority;
- accept or promote candidates;
- modify LoomLoom canon by implication;
- upgrade a project pin;
- turn Research into policy;
- treat runtime success or package verification as acceptance.

If detailed LoomLoom semantics are needed, read the pinned/canonical LoomLoom sources rather than expanding this skill into a duplicate of the kernel documentation.

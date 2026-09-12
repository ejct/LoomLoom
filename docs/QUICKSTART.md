# LoomLoom Quickstart

This is the smallest path for trying LoomLoom on an existing software project.

## 1. Choose an exact LoomLoom release

Use an immutable LoomLoom release/tag. Do not use branch HEAD as a substitute for a release.

For this release candidate the intended public version is:

`v0.3.0-alpha.1`

When the release is tagged, use the exact commit shown by the release/tag as the binding identity.

## 2. Pin LoomLoom in the project

Create `.loomloom/loomloom.lock` using `schemas/loomloom-lock.schema.json` and the example in `fixtures/loomloom.lock.example`.

Conceptually:

```json
{
  "schema_version": 1,
  "repository": "ejct/LoomLoom",
  "commit": "<exact 40-character release commit>",
  "distribution": "github_release",
  "release": "v0.3.0-alpha.1"
}
```

The commit is binding. The release name is descriptive provenance and never overrides the commit.

## 3. Give the agent the Bootstrap

If the runtime supports repository Agent Skills, copy or expose the exact release copy of:

`.agents/skills/loomloom-bootstrap/`

and invoke the `loomloom-bootstrap` skill.

Otherwise give the agent the exact released LoomLoom repository/tag and instruct it to follow `START_HERE.md`.

A useful first instruction is:

> Bootstrap this project with the exact pinned LoomLoom release, emit a LoomLoom Context Receipt, then continue the requested task within the resolved authority and evidence boundaries.

## 4. Expect a Context Receipt

Before authority-sensitive implementation/evaluation work, the agent should resolve and report material state such as:

- LoomLoom identity and exact commit;
- project/task identity;
- material sources actually read;
- authority constraints;
- rigor/topology when material;
- conflicts or missing material context;
- the next bounded action.

`READY` means work can proceed.
`INCOMPLETE` means useful bounded work may continue with limited claims.
`NEEDS_DECISION` means a material authority conflict blocks the requested authority-sensitive action.

The receipt may exist only in the active session when no later actor needs it. When durable continuation/review materially depends on it, reuse a project-native current-state/documentation owner if one exists; otherwise persist the fallback at `.loomloom/context-receipt.yaml`. Do not create duplicate state merely to satisfy LoomLoom.

See `bootstrap/CONTEXT_RECEIPT.md`.

## 5. Run one real bounded task

Start with an existing task where evidence matters: a retained feature, a bug fix, a migration, or another change that you would normally ask a coding agent to implement and verify.

LoomLoom does not require every K1–K12 primitive to become a separate file. Use the project’s existing issue/spec/test/documentation surfaces when they already express the needed semantics.

The practical loop is:

`intent/contract → authorized implementation → exact candidate → observations/evidence → evaluation → explicit acceptance when required → reconciliation`

At task close, reconcile only the durable state needed for a later actor to understand current truth and the next valid action. Verification evidence should normally remain in project-native surfaces such as tests, CI results, build output, version-control state, issue/spec records, or existing evidence documentation. LoomLoom v0.3 does not require a universal post-task evidence schema, evidence receipt, journal, or telemetry file.

## 6. Keep claims proportional to evidence

Examples:

- a unit test does not prove production behavior it did not exercise;
- a page probe does not prove an unpacked browser extension works;
- an agent saying “tests pass” is a claim until tied to an observed exact subject;
- CI success does not accept a candidate;
- a merge does not prove post-integration correctness.

## 7. Upgrade explicitly

When a newer LoomLoom version exists, do not silently follow it. Update the project pin as an explicit project change and re-evaluate any material compatibility differences.

See `VERSIONING.md`.

# LoomLoom agent entry

If the current task involves LoomLoom or a project configured to use LoomLoom:

1. Prefer the `loomloom-bootstrap` Agent Skill when your client supports Agent Skills.
2. Otherwise follow `START_HERE.md`.
3. If `.loomloom/loomloom.lock` exists in the consuming project, resolve that exact pin and do not silently upgrade it.
4. Load only task-relevant LoomLoom context.
5. Emit a LoomLoom Context Receipt before authority-sensitive implementation, evaluation, promotion, or reconciliation work.
6. Research and Archive are not current authority unless the task explicitly requires them.
7. If current sources conflict materially, return `NEEDS_DECISION`.

## Operating behavior

Within the resolved Authority Envelope:

- Be proactive: perform obvious safe, reversible, in-scope next steps without asking for step-by-step direction.
- Tool before human: before shifting a recurring operational step to a person, check available tools, automation paths, alternate runtimes, test harnesses, and lower-privilege execution surfaces.
- Treat repeated human-only build/install/reload/test/observation steps as workflow blockers to reduce.
- Recover from a blocked method: identify the actual blocker and try reasonable alternatives rather than stopping at the first tool limitation.
- Close the loop: after a change, run proportionate available verification, inspect the result, and correct obvious regressions.
- Match claims to evidence fidelity. A surrogate/probe proves only the behavior it exercised.
- Escalate only at real authority, safety, credential, irreversible-side-effect, scope-expansion, or non-delegable decision boundaries.
- Preserve boundedness. Proactivity does **not** authorize unrelated refactors, acceptance, merge, publication, deployment, or scope expansion.
- If human intervention is irreducible, report the exact blocked action, alternatives attempted/considered, and the minimum human action required.

Key invariant: **PROACTIVITY != AUTHORITY ESCALATION**.

## Task profiles

For browser-extension work, read `profiles/browser-extension-development.md` before settling on a human-gated browser test loop.

The bootstrap mechanism has no authority to change LoomLoom canon, project scope, acceptance rules, or release pins.

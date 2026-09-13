# LoomLoom

**Keep coding agents inside the task — and make their work verifiable.**

Coding agents are fast, but consequential work becomes hard to trust when scope drifts, “tests pass” is detached from the exact code that was tested, important state lives only in chat, or the next session has to reconstruct what happened from scratch.

LoomLoom adds a lightweight control layer around the coding agent you already use. It makes scope and decision boundaries explicit, ties verification evidence to the exact code it came from, and leaves enough durable project state for the next agent to continue correctly.

Current distribution: **v0.3.0-alpha.2 — Open Alpha**.

## Start in one command

From the root of an existing project on macOS or Linux:

```sh
curl -fsSL https://raw.githubusercontent.com/ejct/LoomLoom/v0.3.0-alpha.2/install.py -o /tmp/loomloom-install.py && python3 /tmp/loomloom-install.py . && rm -f /tmp/loomloom-install.py
```

The installer resolves the immutable release tag to its exact Git commit, installs the Bootstrap skill into `.agents/skills/loomloom-bootstrap/`, and records that exact identity in `.loomloom/loomloom.lock`. It refuses to silently replace a different pin or overwrite a different existing skill.

Then give your coding agent the task you actually care about:

> Use LoomLoom for this task: fix the cache invalidation bug and verify the result.

You should not need to read LoomLoom documentation, create JSON by hand, or copy files yourself before trying it.

### Or let the agent set it up

Give this to your coding agent from the project root:

> Set up LoomLoom v0.3.0-alpha.2 from https://github.com/ejct/LoomLoom/tree/v0.3.0-alpha.2, using that release’s installer. Pin the exact tagged commit, then use LoomLoom for this task: **<your real task>**.

If your runtime automatically discovers repository Agent Skills, subsequent tasks can stay short. If it does not, tell it to read `.agents/skills/loomloom-bootstrap/SKILL.md` first.

## The problems LoomLoom is for

### “The agent fixed it” — but also changed three unrelated things

LoomLoom resolves the task boundary and authority before consequential work, so capability does not silently become permission.

### “Tests pass” — but what exactly did they prove?

Evidence is tied to an exactly identified candidate. A unit test, page probe, CI run, real-profile check, or production observation can support only the claim it actually exercised.

### The task spans sessions and the next agent starts from folklore

LoomLoom makes the current authoritative state, exact LoomLoom pin, material context, and unresolved constraints recoverable without requiring hidden chat history.

### The agent keeps handing routine verification back to you

Within explicit authority, LoomLoom tells agents to close safe edit → verify → inspect → correct loops themselves and to try lower-interference automation before declaring a routine step human-only.

## What changes in practice

| Without LoomLoom | With LoomLoom |
| --- | --- |
| “Fix this” can expand into whatever the agent thinks is useful | Scope and authority are resolved before consequential work |
| “Tests pass” is a sentence in chat | Evidence refers to the exact candidate it observed |
| CI success, merge, and acceptance blur together | Observation, evaluation, acceptance, and integration stay distinct |
| Important state disappears with the session | Material current state can survive into the next session |
| Every new agent reloads everything “just in case” | Context is loaded selectively when it can change the task or claim |

LoomLoom does not replace your coding agent, Git, CI, issue tracker, tests, or project documentation. It uses those existing surfaces where they already carry the needed truth.

## A normal LoomLoom task

You ask for a real change. The agent should then:

1. resolve the project’s exact LoomLoom pin and material project authority;
2. emit a concise Context Receipt when authority-sensitive work needs it;
3. implement only within the resolved task boundary;
4. verify the exact candidate with evidence proportionate to the claim;
5. ask for a decision only when a real authority boundary requires one;
6. reconcile the smallest durable state needed for correct continuation.

The underlying control model is:

`INTENT → CONTRACT → AUTHORITY → CANDIDATE → OBSERVATION → EVIDENCE → VERDICT → ACCEPTANCE → INTEGRATION → RECONCILIATION`

You do **not** need to learn that model before trying LoomLoom.

## Good first tasks

LoomLoom is most useful when an agent’s mistake, overreach, or unverifiable success claim would cost real time:

- a retained feature or multi-file refactor;
- a bug fix with meaningful regression evidence;
- a migration or dependency change;
- browser-extension work where page behavior and extension-runtime behavior differ;
- a task that will cross sessions or agents;
- work where “done” must be distinguishable from “accepted” or “integrated.”

For a throwaway prototype where you do not care about scope, reproducibility, or future continuation, LoomLoom may be unnecessary overhead.

## What setup adds

```text
.loomloom/
  loomloom.lock

.agents/
  skills/
    loomloom-bootstrap/
```

The lock binds the project to one exact LoomLoom commit. The installed skill is a navigator and operating projection; it does not create authority by itself.

Running setup again for the same release is safe and idempotent. Moving to a different release is an explicit project change, never a silent upgrade.

## Open Alpha boundaries

This is an early Open Alpha. The current release does **not** claim:

- a stable 1.0 API or compatibility promise;
- broad cross-runtime validation;
- a finished generic Kernel implementation;
- automatic acceptance or promotion of agent work;
- that one kind of test proves behavior it did not exercise.

## Go deeper when you need to

You should not need these documents to get started. They exist for deeper operation and verification:

- [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — setup behavior, troubleshooting, and manual details;
- [`docs/DEVELOPMENT_KERNEL.md`](docs/DEVELOPMENT_KERNEL.md) — K1–K12 and the full public control model;
- [`policy/agent-operating-behavior.md`](policy/agent-operating-behavior.md) — agent operating policy projection;
- [`profiles/browser-extension-development.md`](profiles/browser-extension-development.md) — browser-extension evidence and test profile;
- [`VERSIONING.md`](VERSIONING.md) — release and compatibility model;
- [`CHANGELOG.md`](CHANGELOG.md) — public release lineage.

For a released LoomLoom version, the exact Git tag/commit and repository contents at that tag are the public distribution authority.

## Author

Created and maintained by [Victor Cherniavsky](https://github.com/ejct) — Product Designer and UX Architect working on AI-native products, tools, and interaction systems.

## License

MIT. See [`LICENSE`](LICENSE).

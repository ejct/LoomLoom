# LoomLoom

**LoomLoom is an experimental control protocol for agentic software development.** It helps coding agents work autonomously inside explicit authority while keeping evidence, acceptance, and project state tied to exactly identified subjects.

Current distribution: **v0.3.0-alpha.1 — Open Alpha**.

LoomLoom is not a coding agent, a replacement for CI, or a project-management system. It sits above replaceable agent runtimes and gives consequential agent work a small shared control model:

`INTENT → CONTRACT → AUTHORITY → CANDIDATE → OBSERVATION → EVIDENCE → VERDICT → ACCEPTANCE → INTEGRATION → RECONCILIATION`

## Why

Coding agents can generate and modify software quickly. The difficult part is keeping clear answers to questions such as:

- What was the agent actually authorized to change?
- What exact candidate did a test result describe?
- Does a successful run prove the intended claim, or only a narrower surrogate?
- Who is allowed to accept or promote the result?
- Can a fresh agent continue from durable project state without hidden chat history?

LoomLoom makes those boundaries explicit without requiring one specific agent, IDE, CI provider, or repository layout.

## Current alpha

The current public alpha contains:

- Development Kernel v0.1 public specification;
- Bootstrap v0.1 and an Agent Skill;
- exact project pinning and portable package identity;
- Agent Operating Behavior v0.1;
- Browser Extension Development Profile v0.1;
- Context Receipt and selective-context routing;
- validators, fixtures, and tests used by the Bootstrap distribution.

This is an **early open alpha**, not a stable API. Later 0.x releases may change workflow materialization and distribution behavior as dogfood evidence accumulates. The five Kernel invariants and exact-subject/evidence discipline are the current semantic baseline, but no 0.x compatibility promise should be inferred beyond the versioning policy.

## Try it

Start with [`docs/QUICKSTART.md`](docs/QUICKSTART.md).

If your agent supports repository Agent Skills, the distribution includes:

`.agents/skills/loomloom-bootstrap/SKILL.md`

Otherwise use [`START_HERE.md`](START_HERE.md).

A consuming project should pin the exact LoomLoom release/commit in `.loomloom/loomloom.lock` and must not silently upgrade to branch HEAD.

## Public authority

For a released LoomLoom version, the **exact Git tag and the repository contents at that tag are the public distribution authority**. The exact Git commit identifies the released subject.

Important surfaces:

- [`docs/DEVELOPMENT_KERNEL.md`](docs/DEVELOPMENT_KERNEL.md) — public Development Kernel v0.1 specification;
- [`policy/agent-operating-behavior.md`](policy/agent-operating-behavior.md) — accepted operating-policy projection bundled in this distribution;
- [`profiles/browser-extension-development.md`](profiles/browser-extension-development.md) — accepted browser-extension profile projection;
- [`START_HERE.md`](START_HERE.md) — authority-aware entry point;
- [`loomloom.yaml`](loomloom.yaml) — machine-readable distribution metadata;
- [`VERSIONING.md`](VERSIONING.md) — release and component versioning;
- [`CHANGELOG.md`](CHANGELOG.md) — public release lineage.

Internal research, experiments, audit history, and future governance work may exist outside the public release. They are **not required to consume this released version and do not override the tagged public subject**.

## Five invariants

1. **Authority** — No capability creates authority by itself.
2. **Identity** — Evidence always refers to an exactly identified subject.
3. **Observation** — Producer self-report is not independent evidence.
4. **Promotion** — No success signal automatically raises the authority state of an artifact.
5. **Context** — A result cannot be treated as reproducible when its material execution context is unknown.

See [`docs/DEVELOPMENT_KERNEL.md`](docs/DEVELOPMENT_KERNEL.md) for K1–K12, rigor levels, topology, and lifecycle semantics.

## Maturity boundaries

The alpha does **not** claim:

- a finished generic Kernel implementation;
- universal runtime adapters;
- stable multi-runtime compatibility;
- mandatory multi-agent workflows;
- complete autonomous acceptance/promotion;
- that a page probe equals extension-runtime or release/store evidence;
- that runtime/session success implies project acceptance.

LoomLoom deliberately keeps runtime-native session, trace, sandbox, approval, persistence, and subagent mechanics outside the Kernel unless cross-project evidence later justifies a shared abstraction.

## Author

Created and maintained by [Victor Cherniavsky](https://github.com/ejct) — Product Designer and UX Architect working on AI-native products, tools, and interaction systems.

## License

MIT. See [`LICENSE`](LICENSE).

# LoomLoom Development Kernel v0.1

Public specification projection for LoomLoom distributions that declare `kernel: 0.1`.

This document preserves the accepted Development Kernel v0.1 semantics while omitting internal research provenance, audit history, and project-specific source references that are not required to consume the public distribution.

## Purpose

LoomLoom is the project name. Development Kernel is its reusable control-plane architecture for agentic software development. It is not a coding agent, repository template, or project methodology. It defines the minimal protocol, state, evidence, authority, and verification primitives needed to let stochastic agents work quickly inside bounded regions while keeping promotion explicit and evidence-bound.

Canonical lifecycle:

`INTENT → CONTRACT → AUTHORITY → CANDIDATE → OBSERVATION → EVIDENCE → VERDICT → ACCEPTANCE → INTEGRATION → OBSERVATION → RECONCILIATION → CANON / NEXT INTENT`

Core thesis:

Generation may be stochastic, fast, iterative, and highly autonomous inside an authorized region. Promotion must be explicit, attributable, and tied to evidence about an exactly identified subject.

## Distillation rule

A mechanism enters Kernel core only when at least one is true:

A. It recurs in at least two independent workflows.

B. It prevents a real failure class that can recur across projects.

C. It is required for protocol integrity itself, such as exact subject identity.

Everything else remains outside core as an adapter, profile, project policy, module, or experiment topology.

## Kernel primitives

### K1 — Canon

Represent what is authoritative, current, proposed, superseded, or historical. Authority must not be inferred from filename, recency, location, tool capability, branch HEAD, or execution success.

### K2 — Intent

Every meaningful change starts from a machine-addressable intent.

Minimal semantic fields:

- `intent.id`
- `goal`
- `rationale`
- `non_goals`
- `success_conditions`

Intent explains why. It should not prematurely dictate implementation.

### K3 — Contract

A contract defines observable truth and protected behavior.

Minimal semantic fields:

- `requires`
- `preserves`
- `forbids`
- `invariants`
- `acceptance_conditions`

The `preserves` set is first-class: a candidate may satisfy a new requirement while silently breaking existing semantics.

### K4 — Authority Envelope

Every execution has explicit permissions and prohibitions.

Typical fields include:

- `may_read`
- `may_modify`
- `may_create`
- `may_delete`
- `may_execute`
- `must_not_modify`
- `may_publish`
- `may_accept`
- `may_merge`

Authority does not follow automatically from technical capability. An agent being able to push, merge, delete, publish, or deploy does not authorize those actions for a task.

### K5 — Context Receipt

A meaningful agent run records the material context supplied/used for the work.

Typical fields include:

- `canon`
- `task_material`
- `fixtures`
- `prior_evidence`
- `excluded`
- `environment`

High-rigor executions should make the receipt freezeable/hashable when useful. The purpose is to expose material epistemic differences between nominally similar executions, not to duplicate complete runtime traces.

### K6 — Candidate

Builder output is a candidate, never an accepted implementation by default.

Typical fields include:

- `base`
- `identity`
- `produced_by`
- `authority_receipt`
- `changed_surfaces`

Identity may be a Git SHA, content hash, scene revision, schema version, output ID, bundle digest, or another exact subject identity. Kernel is not Git-specific.

### K7 — Execution / Observation

Kernel separates claims from observations.

“Builder says all tests pass” is a claim.

A test run tied to a known candidate and environment is an observation.

Execution harnesses produce observations; runtime-native traces may remain runtime-owned.

### K8 — Evidence

Evidence = observation + provenance + exact subject identity.

Minimal semantic fields:

- `subject`
- `check`
- `observation`
- `producer`
- `environment`
- `timestamp`
- `artifacts`

Evidence without exact subject identity is insufficient for acceptance.

### K9 — Evaluation

Evaluation determines what observations license relative to a contract.

Minimal verdict states:

- `PASS`
- `FAIL`
- `INCONCLUSIVE`

Typical fields include:

- `contract`
- `subject`
- `result`
- `supported_claims`
- `violations`
- `missing_evidence`

`INCONCLUSIVE` is first-class. Missing evidence is neither automatic PASS nor automatic FAIL.

### K10 — Challenge

Challenge is an optional capability that attempts to find counterexamples, break invariants, expose hidden dependencies, invalidate weak evidence, or detect context contamination.

A Challenger does not silently repair the candidate it is challenging.

### K11 — Acceptance

Acceptance is an explicit authority transition.

`PASS ≠ ACCEPTED`

`GREEN CI ≠ ACCEPTED`

`MERGED ≠ ACCEPTED`

`DEPLOYED ≠ CORRECT`

Typical fields include:

- `subject`
- `verdicts`
- `authority`
- `decision`
- `known_deviations`

Typical decisions include `accepted`, `rejected`, and `returned`.

### K12 — Reconciliation

After implementation or production observation, reality may change the canon.

Typical fields include:

- `new_constraints`
- `changed_assumptions`
- `discovered_invariants`
- `documentation_changes`
- `new_evals_required`

Reconciliation closes the lifecycle and prevents durable project truth from drifting permanently away from implementation reality.

## Canonical state machine

Primary states:

`DRAFT → DEFINED → AUTHORIZED → CANDIDATE → OBSERVED → EVALUATED → ACCEPTED → INTEGRATED → RECONCILED`

Side/terminal states:

- `BLOCKED`
- `REJECTED`
- `INCONCLUSIVE`
- `SUPERSEDED`
- `CANCELLED`

State transitions are explicit, never inferred.

CI success must not implicitly perform `EVALUATED → ACCEPTED`.

Merge must not implicitly perform `INTEGRATED → RECONCILED`.

## Capabilities, not mandatory personas

Kernel defines capabilities:

- `DEFINE`
- `PLAN`
- `AUTHORIZE`
- `BUILD`
- `EXECUTE`
- `EVALUATE`
- `CHALLENGE`
- `ACCEPT`
- `INTEGRATE`
- `RECONCILE`

A project/runtime maps actors to capabilities.

A low-risk workflow may let one agent plan, build, execute, and evaluate while a human accepts.

A high-rigor workflow may separate Builder, Runner, Evaluator, Challenger, and Owner contexts.

Separation is policy/topology, not a universal requirement.

## Process configuration

### Rigor

**R0 — Sketch**

`Intent → Build → Run → Human inspect`

Use for disposable exploration.

**R1 — Standard**

`Intent → Contract → Build → Automated checks → Evaluate → Accept`

Default retained-production mode.

**R2 — Controlled**

Adds frozen/exact base where material, explicit authority, protected invariants, independent evaluation where useful, evidence retention, and challenge.

Use for important architecture, data, security, or consequential behavior changes.

**R3 — High Assurance**

Adds strict actor separation where justified, stronger evidence immutability/reproduction, independent audit, strict promotion, and fail-closed evidence requirements.

Use selectively for security-critical, irreversible, or otherwise high-consequence changes.

### Execution topology

- **Integrated** — one context may plan, build, run, and evaluate.
- **Separated** — builder and evaluator are separate actors/contexts.
- **Parallel** — several candidates or evaluations run independently.
- **Adversarial** — a Challenger attempts to invalidate the result.
- **Blinded** — selected actors are intentionally denied oracle or privileged context.

Rigor and topology are independent axes.

## Five fundamental invariants

### I1 — Authority

No capability creates authority by itself.

### I2 — Identity

Evidence always refers to an exactly identified subject.

### I3 — Observation

Producer self-report is not independent evidence.

### I4 — Promotion

No success signal automatically raises the authority state of an artifact.

### I5 — Context

A result cannot be treated as reproducible when its material execution context is unknown.

Together these form the semantic safety model of the Kernel.

## Deliberately not mandatory in v0.1

Do not universalize these as Kernel requirements without additional evidence:

- one universal task-file format;
- one universal agent prompt;
- mandatory Challenger;
- mandatory independent Evaluator;
- mandatory immutable evidence retention;
- mandatory GitHub integration;
- mandatory documentation hierarchy;
- mandatory multi-agent workflow;
- runtime-owned session/trace/sandbox/approval/persistence/subagent mechanics.

Projects may materialize K1–K12 through existing issues, specifications, tests, CI, docs, runtime tools, and project-native state. Semantic primitives do not imply one file/object per primitive.

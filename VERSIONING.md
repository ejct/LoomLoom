# LoomLoom Versioning

LoomLoom uses three distinct identities: distribution version, component version, and exact subject identity.

## Distribution version

Public LoomLoom distributions use Semantic Versioning syntax:

`MAJOR.MINOR.PATCH[-prerelease]`

Example:

`0.3.0-alpha.1`

Before `1.0`, compatibility is intentionally conservative:

- **MINOR** — a material change to public workflow/distribution semantics that may change how a consuming project or agent should behave;
- **PATCH** — a compatible correction that does not change the public operating contract materially;
- **prerelease** (`alpha.N`, later `beta.N`/`rc.N`) — maturity channel and iteration within the same intended semantic release line.

A later release must not be inferred to be compatible merely because it is newer. Consuming projects should pin exact LoomLoom identity and upgrade explicitly.

## Component versions

Major LoomLoom components/specifications evolve independently from the distribution version.

Examples:

- Development Kernel v0.1
- Bootstrap v0.1
- Agent Operating Behavior v0.1
- Browser Extension Development Profile v0.1

A distribution such as LoomLoom `0.4.2` may legitimately still contain Development Kernel `0.1` while bundling a newer policy/profile component.

Component version changes do not automatically determine the distribution bump; the distribution bump follows the material compatibility impact of the bundled public subject.

## Exact subject identity

A human-readable version does not replace exact identity.

For Git releases:

`version/tag → exact Git commit`

For detached portable packages, `loomloom-package.json` provides content identity according to `bootstrap/PACKAGE_IDENTITY.md`.

The exact subject is what evidence, validation, and project pins ultimately bind to.

## Internal lineage before the first public release

LoomLoom developed through several unpublished semantic generations before opening the repository as a public distribution:

- **0.1 internal generation** — Development Kernel foundation: K1–K12, lifecycle, authority/evidence/promotion semantics, rigor/topology, five invariants.
- **0.2 internal generation** — runtime boundary and Bootstrap direction: Probe Before Abstraction, exact pinning/package identity, selective bootstrap, versioned GitHub distribution.
- **0.3 generation** — current shippable distribution: integrated Bootstrap plus accepted operating/profile projections and public self-contained packaging.

No retrospective public Git tags are created for the unpublished 0.1/0.2 generations.

The first intended public open-alpha release is therefore:

`v0.3.0-alpha.1`

A future `0.4.0-*` should correspond to a material accepted distribution-semantic change, not merely elapsed time, additional research, or internal proposal churn.

## Release metadata

`loomloom.yaml` is the machine-readable owner of distribution version/channel and bundled component versions.

It does not self-attest the Git commit containing it. Exact Git identity comes from the immutable release tag/ref and commit metadata.

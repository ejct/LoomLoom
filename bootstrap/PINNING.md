# LoomLoom Project Pinning

A consuming project may pin LoomLoom with `.loomloom/loomloom.lock`.

The lock is a small JSON document conforming to `schemas/loomloom-lock.schema.json`.

## Required semantics

- `repository` identifies the LoomLoom repository as `owner/name`.
- `commit` is the binding identity and MUST be an exact 40-character Git commit SHA.
- `distribution` records whether the pin came from an immutable Git commit or a named GitHub release.
- `release` is optional descriptive provenance. A release/tag name never overrides `commit`.

## Validation vs repository resolution

`scripts/validate_loomloom_pin.py` validates and normalizes the lock into a pinned identity of the form `repository@commit`.

It deliberately does **not** contact GitHub/Git or prove that the commit exists or is accessible. Repository availability belongs to the consuming runtime/repository adapter.

When `.loomloom/loomloom.lock` exists:

1. parse and validate the lock;
2. establish the exact pinned identity `repository@commit`;
3. through the current repository adapter/runtime, verify that the exact commit is accessible before authority-sensitive use;
4. do not substitute branch HEAD, a newer release, or current LoomLoom governance state;
5. record the exact commit actually used in the Context Receipt;
6. if the exact commit is unavailable or conflicts with another binding authority source, fail closed rather than silently falling forward;
7. return `NEEDS_DECISION` when an authority-sensitive action requires choosing a different LoomLoom identity.

The lock does not grant permission to update itself. Updating a project pin is an authority-sensitive project change.

## No project pin

If no lock exists, use an explicit task/project LoomLoom identity when supplied. Otherwise use the current accepted release available to the agent and record the exact commit actually used. Repository HEAD is not an accepted release merely because it is newer.

## Example

See `fixtures/loomloom.lock.example`. Its values are illustrative only and carry no authority.

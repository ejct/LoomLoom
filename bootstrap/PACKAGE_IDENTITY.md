# LoomLoom Portable Package Identity

Git repository distributions are identified by their exact Git commit.

A detached/portable LoomLoom directory or archive cannot rely on Git metadata, so it may carry a generated `loomloom-package.json` manifest.

This manifest is packaging metadata, not a new LoomLoom protocol primitive or authority source.

## Manifest semantics

`loomloom-package.json` contains:

- `schema_version`;
- optional `source_commit` when the package was produced from a Git checkout;
- `content_digest`;
- a sorted map of relative file paths to SHA-256 digests.

The manifest file itself and `.git/` are excluded from the digest set, avoiding self-reference.

`content_digest` is SHA-256 over canonical JSON for the sorted file-hash map.

`source_commit` is **descriptive provenance only**. It is not included in `content_digest`, is not independently verified by package-content verification, and must not be treated as source-commit attestation, authenticity, signature, or proof that the package was produced from that commit.

A consumer may verify the manifest before using a portable snapshot. Verification establishes package-content identity only: the current file set matches the file hashes and aggregate digest recorded in the manifest. It does not make the package current, accepted, authentic, or authoritative beyond the authority explicitly assigned to that snapshot.

Use `scripts/package_identity.py create` to generate the manifest and `scripts/package_identity.py verify` to verify it.

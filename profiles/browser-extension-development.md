# Browser Extension Development Profile

Status: candidate distribution projection of accepted LoomLoom project profile `06 — Decision — Browser Extension Development Profile` / Drive profile `Browser Extension Development Profile v0.1`.

This file is operational guidance, not independent semantic authority.

## Core rules

- Prefer **agent-closed verification** loops whenever technically possible.
- Treat recurring human-only install/reload/navigation/test steps as workflow blockers to reduce, not normal iteration assumptions.
- Use the **cheapest faithful probe first**, but never promote low-fidelity evidence into higher-fidelity claims.
- Keep page/feature logic separable from the extension shell where practical.
- Isolate volatile host-page assumptions behind a Host Adapter boundary.
- Require idempotent injection, cleanup, and remount behavior for SPA-oriented content scripts.
- Design Manifest V3 background logic to survive normal service-worker termination/restart.
- Minimize permissions, privileged message surfaces, and web-accessible resources.

## Verification ladder

### P0 — Pure/unit
Use for logic that does not require browser/extension semantics.

### P1 — Page rapid probe
Use CDP/evaluate injection, console/page script, or a **bookmarklet** for page-local hypotheses.

Bookmarklets are explicitly useful when privileged extension install/reload controls are unavailable to the agent. They can move a repeated test step into a page execution surface the agent can operate.

Good P1 targets: selectors, Host Adapter behavior, MutationObserver logic, injected UI, SPA lifecycle assumptions, mount/unmount, and page-local interactions.

### P2 — Dev extension runtime
Prefer a hot-reload/fast-reload development runtime such as WXT, CRXJS, or equivalent when appropriate.

### P3 — Extension lifecycle automation
Use Chrome DevTools MCP or equivalent extension lifecycle tooling when available. Current Chrome DevTools MCP supports tools such as `install_extension`, `reload_extension`, `list_extensions`, `trigger_extension_action`, and `uninstall_extension` when extension tools are enabled.

### P4 — Automated extension E2E
Use Playwright Chromium or equivalent controlled extension runtime for repeatable MV3/service-worker/extension-page tests.

### P5 — Real user browser/profile
Reserve human-gated real-profile verification for behavior that cannot be faithfully reproduced by agent-operable surfaces. Do not make P5 the normal edit-test loop.

## Human-gate recovery order

Before asking a human to reload/install/restart an extension, check as relevant:

1. existing HMR/dev-server capability;
2. extension lifecycle tooling such as Chrome DevTools MCP;
3. controlled Playwright/Chromium runtime;
4. direct CDP/page injection;
5. bookmarklet/console injection or a narrow dev-only bridge;
6. only then an irreducible human-gated browser action.

If human action remains necessary, report why reasonable autonomous alternatives are unavailable or insufficient.

## Evidence fidelity

`PAGE_PROBE PASS != EXTENSION_RUNTIME PASS != RELEASE/STORE PASS`

Label the exercised surface. Page injection can validate page-local behavior but does not verify `chrome.runtime`, service-worker lifecycle, permissions, isolated-world semantics, extension CSP, install/update behavior, or store compatibility.

## Host Adapter

Centralize unstable host-specific assumptions:

`feature logic -> host adapter -> host DOM/API`

Prefer semantic resolvers such as `resolveComposer()` or `resolveConversationTurn()` over raw selectors scattered across features. Useful diagnostics include `FOUND`, `NOT_FOUND`, `AMBIGUOUS`, `UNSUPPORTED_VARIANT`, and `STALE_TARGET`.

## SPA / injection invariants

Verify initial load, internal navigation, back/forward, target element recreation, lazy/virtualized content, repeated mount, extension reload while the page remains open, cleanup, and remount.

Target invariants:

- `mount -> mount` results in one effective mount;
- `mount -> unmount -> mount` returns to a clean equivalent state;
- no duplicate UI, observers, handlers, timers, or stale detached-node state.

## MV3 service worker

Assume routine worker termination. Do not keep durable state only in globals. Reconstruct/reload state when the worker wakes and explicitly test termination/restart for workflows that depend on background state.

## Privilege boundary

Treat content-script/page-originated messages as untrusted input. Validate message type/payload, allowlist privileged operations, constrain arguments, avoid arbitrary URL/action forwarding, and keep secrets/high-value data outside page scope.

## Permissions and storage

Use least privilege. Prefer optional permissions/host permissions where capability can be requested at point of use.

Choose storage by semantics:

- `storage.sync`: compact user preferences;
- `storage.local`: durable extension-local data;
- `storage.session`: ephemeral runtime/session state where appropriate.

## UI isolation

Choose deliberately:

- integrated DOM/CSS for intentionally host-native UI;
- Shadow DOM for extension-owned UI needing CSS isolation;
- iframe for stronger isolation when direct host integration is less important.

## Lifecycle test matrix

Select relevant cases from: fresh install, extension reload, page reload, SPA navigation, service-worker termination/revival, browser restart, extension update/migration, permission grant/denial/revocation, host DOM variation, disable/re-enable, popup/side-panel lifecycle, and network/offline failure.

## Release gate

When distribution is in scope, verify production manifest/package, removal of dev-only bridges/debug permissions, least privilege, permission-warning changes, remote-code/CSP compliance, privacy/data disclosures, store policy compatibility, package installability, update/migration behavior, and store draft validation where available.

## Current implementation references

Tool-specific facts change and must be rechecked in the actual environment. Current useful references include Chrome DevTools MCP extension tools, WXT fast dev/HMR, and Playwright Chromium extension testing. These are implementation options, not LoomLoom Kernel semantics.

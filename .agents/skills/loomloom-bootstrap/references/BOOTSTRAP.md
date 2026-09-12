# LoomLoom Bootstrap Procedure

Use this procedure when asked to:

- bootstrap LoomLoom;
- enter a new chat or agent into LoomLoom context;
- initialize a LoomLoom-governed task;
- recover the current LoomLoom authority state.

## Procedure

1. **Classify the mode**
   - consumer project;
   - LoomLoom development;
   - portable snapshot.

2. **Resolve LoomLoom identity**
   - In a consumer project, look first for `.loomloom/loomloom.lock`.
   - When the lock exists, validate it and resolve exactly the pinned `repository@commit`; see `PINNING.md`.
   - Never substitute branch HEAD, a newer release, or current governance state for a binding project pin.
   - In LoomLoom development, resolve current owner decisions/status first.
   - In portable mode, verify supplied package identity when a `loomloom-package.json` manifest is present; see `PACKAGE_IDENTITY.md`.
   - Never infer authority from "latest file" or repository HEAD alone.

3. **Read the entry map**
   - `START_HERE.md` for repository distribution.
   - Drive `01 — Status & Decisions` for LoomLoom workspace development.

4. **Resolve task scope**
   Identify what the user is actually trying to do.

5. **Apply operating behavior**
   Work proactively inside authority. Use available tools/automation and reasonable alternate execution surfaces before accepting recurring human-gated steps. Diagnose blocked methods and close the verification loop when possible. Proactivity never creates authority.

6. **Load selectively**
   Use `ROUTING.md`.
   Load only sources that materially change execution, evaluation, authority, or interpretation.

7. **Detect conflicts**
   Examples:
   - pinned project release differs from latest release;
   - Drive accepted release points to commit A while local/GitHub HEAD is B;
   - an archived proposal contradicts current canon;
   - a research note appears more recent than an accepted decision.

   Do not auto-resolve material authority conflicts.

8. **Emit Context Receipt**
   Use `CONTEXT_RECEIPT.md`.
   Record the exact resolved commit/package identity used for the task.

9. **Proceed under resolved rigor/topology**
   The bootstrap process may recommend a rigor/topology, but it cannot grant itself authority.

## Non-goals

The bootstrap does not:

- summarize all LoomLoom history;
- upgrade a project pin;
- promote research into canon;
- accept candidates;
- merge or deploy;
- create a second copy of LoomLoom semantic truth;
- treat package verification as proof that a snapshot is current or accepted.

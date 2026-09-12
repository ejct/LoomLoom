# LoomLoom Context Receipt

Emit this before substantive authority-sensitive work.

```yaml
loomloom_context_receipt:
  status: READY | NEEDS_DECISION | INCOMPLETE

  mode: consumer_project | loomloom_development | portable_snapshot

  loomloom_identity:
    source: github_release | project_pin | drive_workspace | portable_capsule
    version: null
    commit: null
    canonical_baseline: null

  project_identity:
    repository: null
    base: null
    loomloom_lock: null

  task:
    summary: ""
    task_type: ""
    requested_outcome: ""

  sources_read: []
  relevant_decisions: []
  excluded_as_non_material: []

  execution:
    rigor: R0 | R1 | R2 | R3 | unresolved
    topology: []
    authority_constraints: []

  conflicts: []
  missing_material_context: []

  interpretation:
    current_truth: ""
    next_action: ""
```

## Rules

- `READY` means the agent knows enough material context to proceed.
- `INCOMPLETE` means useful work may continue, but claims must be bounded.
- `NEEDS_DECISION` means a material authority conflict blocks the requested authority-sensitive action.
- Never claim a source was read when it was not actually accessed.
- Keep the receipt concise; it is an execution aid, not a project summary.

## Persistence

The receipt does not require a universal storage system.

- Emitting it in the active agent/session is sufficient when no later actor needs to reconstruct the decision context.
- When durable continuation, review, or audit materially depends on the resolved context, persist the receipt in an existing project-native current-state/documentation surface when one clearly owns that information.
- If no adequate project-native owner exists, use `.loomloom/context-receipt.yaml` as the default project-local fallback.
- Do not create duplicate receipt/state files merely because LoomLoom is present.

## Post-task reconciliation and evidence

The Context Receipt is not a universal evidence log or execution transcript.

After material work, reconcile durable project state only as needed so a later actor can determine the current truth and next valid action. The receipt may be updated in place when it is the appropriate owner of that context, especially `interpretation.current_truth` and `interpretation.next_action`.

Keep verification evidence in the project's existing evidence surfaces where practical: tests, CI results, build output, version-control state, issue/spec records, or other project-native artifacts. Preserve enough exact-subject and environment information to keep claims bounded and reproducible.

LoomLoom v0.3 does not require a universal post-task evidence schema. Do not introduce a new evidence receipt, journal, or telemetry file solely to satisfy Bootstrap.

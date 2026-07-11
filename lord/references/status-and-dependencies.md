# Task Status and Dependencies

## 1. `task_status` Values

- `PENDING`: Prerequisites are not satisfied.
- `READY`: Dependencies are satisfied and the task can be dispatched.
- `IN_PROGRESS`: A Serf executor is executing the task.
- `BLOCKED`: Required input, dependency, permission, runtime, or decision is missing.
- `REVIEW`: A REVIEW submission report awaits Lord review.
- `REWORK`: Lord requires a corrected execution.
- `DONE`: Lord accepted the outputs.
- `REJECTED`: Lord rejected the output or approach.
- `CANCELLED`: The project no longer requires the task.

## 2. Normal Flow

```text
PENDING → READY → IN_PROGRESS → REVIEW → DONE
```

Common exception flows:

- `IN_PROGRESS → BLOCKED`
- `REVIEW → REWORK → IN_PROGRESS`
- `REVIEW → REJECTED`
- `PENDING | READY → CANCELLED`

## 3. Status and Submission Separation

Serf submits `REVIEW`, `BLOCKED`, or `CHANGE_REQUEST`. These are `submission_type` values, not authoritative task outcomes.

Task packages, submission reports, and chat may describe state, but only the authoritative state source controls `task_status`. Lord performs every authoritative update.

## 4. Dependency Checks

Before setting `READY`, confirm:

- Required inputs exist.
- Upstream tasks reached the required state.
- Required upstream submission reports are readable.
- Shared interfaces are defined.
- The task version and runtime are current.

## 5. Parallel Execution

Allow parallel execution only when:

- Tasks do not modify the same controlled files.
- Tasks do not depend on unfinished outputs from one another.
- Shared interfaces are frozen or explicit.
- Work boundaries do not overlap.
- Lord has confirmed there is no conflict.

## 6. Blockers and Change Requests

A missing required dependency produces `BLOCKED`. Optional information may use a reversible documented assumption only when it cannot change scope, interfaces, output meaning, or acceptance.

For `CHANGE_REQUEST`, set `task_status: BLOCKED` only when work cannot continue within the current boundary; otherwise retain `IN_PROGRESS` while Lord decides.

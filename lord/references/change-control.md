# Change Control

## 1. Local Adjustments

A Serf executor may make local, reversible adjustments that do not affect public interfaces, architecture, shared data, shared paths, acceptance meaning, or another task. Record each adjustment in the submission report.

## 2. CHANGE_REQUEST Required

Serf must submit `CHANGE_REQUEST` before changing:

- Public interfaces or schemas.
- Architecture or shared data structures.
- Shared paths or files owned by another task.
- Task scope, acceptance criteria, or validation strategy.
- Security, migration, rollback, or irreversible behavior.

The report must state whether work can continue inside the current boundary while Lord decides.

## 3. Required Contents

Include only:

- The smallest requested change.
- Why current execution is unsafe or incomplete without it.
- Affected files, interfaces, tasks, rollback, and validation.
- Whether execution is blocked.
- The needed decision.

## 4. Lord Decision

Use one decision value:

- `APPROVE_CHANGE`
- `REJECT_CHANGE`
- `REQUEST_INFO`

If the request blocks execution, Lord sets `task_status: BLOCKED`; otherwise the task remains `IN_PROGRESS`. After a decision, Lord updates the authoritative state source, task package version, affected interfaces, dependencies, and downstream tasks before execution resumes.

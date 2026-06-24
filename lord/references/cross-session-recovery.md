# Cross-Session Recovery

## 1. Recovery Order

1. Read the project overview.
2. Read the authoritative task state source.
3. Read the latest architecture and interface files.
4. Find tasks in `IN_PROGRESS`, `REVIEW`, `BLOCKED`, or `REWORK`.
5. Read the corresponding task files, dispatch files, and handoffs.
6. Check task versions.
7. Read recent decisions, issues, and changes.
8. Generate a recovery summary.
9. Only then continue dispatch, review, or task splitting.

## 2. Recovery Summary

Include at least:

- Current project phase.
- Completed tasks.
- Tasks in progress.
- Tasks awaiting review.
- Blocked tasks.
- Rework tasks.
- Tasks ready to start.
- Recent architecture or interface changes.
- Current main risks.
- Recommended next step.

## 3. Prohibited Actions

Before recovery is complete, do not:

- Reuse an existing task ID.
- Recreate the same task.
- Refactor existing architecture immediately.
- Ignore unreviewed handoffs.
- Continue dispatch based on an old task version.

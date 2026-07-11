# Shared Workspace Adapter

## Paths

- Store task packages under `TASKS/`.
- Store dispatch instructions under `DISPATCH/` when persistent dispatch records are needed.
- Store REVIEW reports under `REVIEWS/`.
- Store BLOCKED reports under `BLOCKERS/`.
- Store CHANGE_REQUEST reports under `CHANGE_REQUESTS/`.

Use repository-root-relative paths in protocol artifacts.

## Write Safety

- Do not overwrite another task package or submission report.
- Write only inside assigned paths.
- Use atomic writes when partial files could be observed by another process.
- Preserve the task version in each submission.

## Parallel Safety

Parallel execution requires disjoint controlled paths, frozen shared interfaces, no unfinished cross-dependency, and Lord confirmation.

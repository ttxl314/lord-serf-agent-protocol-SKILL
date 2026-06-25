# Shared Workspace Agent Adapter

Use when multiple agents can access the same repository, cloud drive, or project directory.

## Dispatch Requirements

- Use paths relative to the project root.
- Check task version and the authoritative state source before work starts.
- Write formal task files to `TASKS/`.
- Write launch instructions to `DISPATCH/`.
- Write `REVIEW` reports to `HANDOFFS/`.
- Write `BLOCKED` reports to `BLOCKERS/`.
- Write `CHANGE_REQUEST` reports to `CHANGE_REQUESTS/`.
- Do not re-upload files already available in the shared directory.
- Do not overwrite another agent's task or report file.

## Parallel Limits

Parallel agents must have non-overlapping controlled file scopes or use separate branches/worktrees.

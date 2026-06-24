# Shared Workspace Agent Adapter

Use when multiple agents can access the same repository, cloud drive, or project directory.

## Dispatch Requirements

- Use paths relative to the project root.
- Check task version and the authoritative state source before work starts.
- Write formal task files to `TASKS/`.
- Write launch instructions to `DISPATCH/`.
- Write handoffs to `HANDOFFS/`.
- Write blockers to `BLOCKERS/`.
- Do not re-upload files already available in the shared directory.
- Do not overwrite another agent's handoff or task file.

## Parallel Limits

Parallel agents must have non-overlapping controlled file scopes or use separate branches/worktrees.

---
name: lord
description: >
  Use when Codex must act as the Lord orchestrator for complex multi-agent work
  across software, platforms, or independent sessions: analyze architecture,
  create Task-A-01 style task packages, dispatch Serf executors through
  capability adapters, manage dependencies and submission reports, review
  results, recover project state, and maintain one authoritative state source.
  Do not use for ordinary one-shot tasks, simple local edits, or work that does
  not require cross-executor coordination or persistent project state.
---

# Lord

## Core Contract

Use this skill to convert a complex project into platform-neutral task packages for Serf executors. Keep project state in files, not chat memory.

Lord owns planning, task packages, dispatch, authoritative task state, review decisions, and final acceptance. Serf owns bounded execution of one task package and produces one submission report.

Lord must:

- Understand goals, scope, constraints, non-goals, deliverables, architecture, interfaces, and risks.
- Select the smallest sufficient project structure and task profile.
- Split work into bounded tasks with explicit dependencies, versions, boundaries, outputs, acceptance criteria, and validation methods.
- Keep each task large enough to be an independently verifiable project contribution; merge sibling work when correctness would require reconstructing their combined intent.
- Assign task IDs as `Task-[subproject-letter]-[sequence]`, such as `Task-A-01`.
- Select one dispatch mode and one capability adapter.
- Generate task packages, launch instructions, and expected submission paths.
- Review actual outputs and evidence before updating the authoritative state source.

Serf submits only `REVIEW`, `BLOCKED`, or `CHANGE_REQUEST`. Lord alone sets authoritative outcomes such as `REWORK`, `DONE`, `REJECTED`, or `CANCELLED`.

## Workflow

1. Initialize or recover the project. For recovery, read `references/cross-session-recovery.md` before changing tasks.
2. Analyze architecture and interfaces enough to split work safely.
3. Select project scale and files using `references/project-scaling.md`.
4. Create or update the authoritative state source before dispatch.
5. Assign task IDs such as `Task-A-01`, `Task-A-02`, and `Task-B-01`; each subproject letter starts at `01`.
6. Select `micro`, `standard`, or `full`.
7. Select `direct`, `semi-automatic`, or `manual-copy` using `references/dispatch-modes.md`.
8. Select one adapter identifier: `generic-chat`, `coding`, `document`, `api`, or `shared-workspace`. Load the matching file from `references/adapters/`.
9. Generate the smallest sufficient task package:
   - Use `assets/templates/micro-task.yaml` for `micro`.
   - Use `assets/templates/task-package.md` for `standard` or `full`, omitting sections that do not apply.
   - Include a compact project context index: the project goal, this task's role, related task IDs, and only the repo-root paths needed for alignment.
   - Validate machine-readable packages with the matching schema under `assets/schemas/`.
10. Generate `assets/templates/dispatch-instruction.md`. Start with `$serf` when supported and point to the task package instead of restating it.
11. Process Serf submissions with the canonical templates and schemas in the active Serf skill.
12. Adapt output language using `references/output-language-and-cjk-code.md`.
13. Review outputs using `references/review-and-acceptance.md`, then update the authoritative state source.

## Task Profiles

Use `micro` only when all are true:

- One clear, low-risk objective.
- No more than two non-trivial files.
- No public interface, architecture, shared-data, or shared-path change.
- No complex dependency or overlapping file ownership.
- No more than three acceptance criteria.

Use `standard` for ordinary module-level work, several related files, simple dependencies, or routine validation.

Use `full` for architecture, public interfaces, shared schemas or configuration, multiple coordinated tasks, security-sensitive work, difficult rollback, or complex recovery.

## Context Economy

- Reference authoritative files instead of repeating stable context.
- For `micro`, encode the context index in `objective`, `depends_on`, and `inherits`; do not add parallel fields.
- Keep launch instructions to the task path and essential runtime note.
- Use stable acceptance IDs and reuse evidence across criteria.
- Use delta-only rework instructions.
- Escalate profiles only when risk, interfaces, dependencies, or coordination require it.

## Non-Negotiables

- Never claim a Serf executor was dispatched unless an API, connector, automation, or user action actually started it.
- Keep one authoritative state source: `TASKS.md`, `PROJECT_PLAN.md`, or `TASK_REGISTRY.yaml`.
- Treat task packages as requirements and Serf submission reports as evidence; neither replaces authoritative state.
- Require protocol `0.5`, `project_id`, `task_id`, `task_version`, `updated_at`, and `task_status` in every task package.
- Do not mix v0.3 field names or paths into v0.5 artifacts.
- Never use `agent_id`, `Agent-A-01` IDs, `assigned_to`, `.agents/` paths, `status` as a task-package field, or an adapter name outside the canonical five identifiers.
- Use `REVIEWS/[task_id]-REVIEW.yaml` for `micro` and `REVIEWS/[task_id]-REVIEW.md` for `standard` or `full` unless the project defines another explicit `submission_path`.
- Require each submission to copy `profile`, use `executed_task_version`, and match the assigned `task_id`.
- For Python tasks, specify a conda environment path, exact Python executable, or activation command.
- If a change request prevents further execution, set the task to `BLOCKED`; otherwise keep it `IN_PROGRESS` while Lord decides.
- Use `APPROVE_CHANGE`, `REJECT_CHANGE`, or `REQUEST_INFO` for change decisions.
- Default output language to the current conversation language unless the user specifies another.
- Check encoding and CJK hazards for code tasks involving localized text, names, paths, comments, or data.

## Load As Needed

- Project scale and profiles: `references/project-scaling.md`
- Cross-platform pairing: `references/cross-platform-pairing.md`
- Task status and dependencies: `references/status-and-dependencies.md`
- Dispatch modes: `references/dispatch-modes.md`
- Output language and CJK hygiene: `references/output-language-and-cjk-code.md`
- Change control: `references/change-control.md`
- Review and acceptance: `references/review-and-acceptance.md`
- Cross-session recovery: `references/cross-session-recovery.md`
- Capability adapters:
  - `references/adapters/generic-chat.md`
  - `references/adapters/coding.md`
  - `references/adapters/document.md`
  - `references/adapters/api.md`
  - `references/adapters/shared-workspace.md`
- Templates:
  - `assets/templates/project-overview.md`
  - `assets/templates/project-plan.md`
  - `assets/templates/micro-task.yaml`
  - `assets/templates/task-package.md`
  - `assets/templates/dispatch-instruction.md`
  - `assets/templates/recovery-summary.md`
- Schemas:
  - `assets/schemas/micro-task.schema.yaml`
  - `assets/schemas/task-package.schema.yaml`
  - `assets/schemas/dispatch-instruction.schema.yaml`
- Canonical Serf submission assets:
  - `assets/templates/micro-review-report.yaml`
  - `assets/templates/review-report.md`
  - `assets/templates/blocker-report.md`
  - `assets/templates/change-request-report.md`
  - `assets/schemas/submission-envelope.schema.yaml`
  - `assets/schemas/micro-review-report.schema.yaml`
  - `assets/schemas/review-report.schema.yaml`

The final group is relative to the active Serf skill root.

## Minimum Orchestration Output

For a simple dispatch, include only project and task IDs, profile, task package path, task status, dependencies, target adapter, dispatch mode, submission path, and a short launch instruction.

For initialization, recovery, architecture changes, or multi-task coordination, also include project scope, selected structure, architecture summary, task relationships, risks, blockers, and next steps.

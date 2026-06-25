---
name: lord
description: >
  Use when Codex must act as a master planning agent to orchestrate complex
  multi-agent work across external software, platforms, or independent sessions:
  analyze architecture, split projects into Agent-A-01 style tasks, generate
  portable task packages, adapt launch instructions by agent capability, manage
  handoffs/blockers/change requests, recover projects across sessions, and
  maintain a single authoritative project plan or task registry. Do not use for
  ordinary one-shot tasks, simple local edits, or work that does not require
  cross-agent delegation or project-state coordination.
---

# Lord

## Core Contract

Use this skill to turn a complex project into platform-neutral task packages for external agents. Keep project state in files, not chat memory.

Paired skill: use `serf` as the recommended execution-side worker skill for agents that receive lord-issued task packages. For cross-platform use, see `references/cross-platform-pairing.md`.

The master agent must:

- Understand project goals, scope, constraints, non-goals, and deliverables.
- Analyze architecture, modules, data flow, interfaces, shared resources, and risks.
- Select the smallest sufficient project structure from `references/project-scaling.md`.
- Select the smallest sufficient task profile: `micro`, `standard`, or `full`.
- Split work into bounded tasks with dependencies, versions, and acceptance criteria.
- Assign IDs with `Agent-[subproject-letter]-[sequence]`, such as `Agent-A-01`.
- Select a dispatch mode and a capability-based adapter.
- Generate task packages, launch instructions, and return templates.
- Review external agent outputs and update the single authoritative state source.

External agents may submit `REVIEW`, `BLOCKED`, or change requests. Only the master agent may confirm `DONE`, `REJECTED`, or `CANCELLED`.

## Workflow

1. Initialize or recover the project. For recovery, read `references/cross-session-recovery.md` before creating or changing tasks.
2. Analyze architecture and interfaces enough to split work safely.
3. Select scale and files from `references/project-scaling.md`.
4. Create or update the authoritative project plan or task registry before dispatch.
5. Assign IDs as `Agent-A-01`, `Agent-A-02`, `Agent-B-01`; each subproject letter starts at `01`.
6. Select a task profile:
   - `micro` for small, low-risk, isolated work.
   - `standard` for ordinary module-level work.
   - `full` for architecture, shared interfaces, complex dependencies, high risk, or multi-agent coordination.
7. Pick a dispatch mode from `references/dispatch-modes.md`: direct, semi-automatic, or manual copy.
8. Pick one capability adapter from `references/adapters/`. Do not create brand-specific adapters unless capability rules differ.
9. Generate the smallest sufficient task package:
   - Use `assets/templates/micro-task.yaml` for `micro`.
   - Use `assets/templates/agent-task.md` for `standard` or `full`, omitting sections that do not apply.
   - Validate `micro` packages with `assets/schemas/micro-task.schema.yaml`; use the full schemas for `standard` or `full` machine-readable packages.
10. Generate launch instructions that start with `$serf` when the target platform supports skill-style invocation, then point to the formal task package instead of restating a second source of truth.
11. Process handoffs, blockers, and change requests with the templates in `assets/templates/`.
12. Adapt output language using `references/output-language-and-cjk-code.md`.
13. Review actual outputs using `references/review-and-acceptance.md`; update the authoritative state source only after review.

## Context Economy

- Use the smallest task profile that can be executed safely.
- Do not generate empty sections.
- Do not repeat project-level context already available through referenced files.
- Prefer file references over pasted content.
- Keep launch instructions short and point to the formal task package.
- Use concise delta instructions for rework instead of restating the whole task.
- Give acceptance criteria stable IDs when evidence must be mapped back to them.
- A low-risk task package should not be substantially longer than the work description and acceptance evidence combined.
- Escalate from `micro` to `standard` or `full` only when risk, dependencies, interfaces, or coordination require it.

## Task Profile Selection

Use `micro` when all are true:

- The task has one clear objective.
- It changes no more than 2 files, unless the files are trivial and tightly related.
- It does not change public interfaces, architecture, shared data structures, or shared paths.
- It has no complex upstream or downstream dependency.
- It has no overlapping controlled-file ownership with another active task.
- It has no more than 3 acceptance criteria.

Use `standard` when the task involves ordinary module-level work, several related files, simple dependencies, or routine build/test validation.

Use `full` when any of these apply:

- Public interface or architecture changes.
- Shared database, schema, configuration, or data-structure changes.
- Multiple subprojects or external agents must coordinate.
- High-risk, difficult-to-reverse, or security-sensitive work.
- Complex change approval, rollback, or recovery requirements.

## Non-Negotiables

- Never claim an external agent has been started unless the current environment directly invoked it through a verified API, connector, or automation.
- Keep one authoritative state source: `TASKS.md`, `PROJECT_PLAN.md`, or `TASK_REGISTRY.yaml`, depending on project scale.
- Treat task files as requirements and handoff files as submissions; neither overrides the authoritative state source.
- Require `project_id`, `agent_id`, `task_version`, and `updated_at` in task packages.
- For Python tasks, specify the conda environment path, exact Python executable, or activation command so external agents can run the same runtime.
- Require handoffs to include `executed_task_version`; do not accept stale-version results directly.
- Make required files, inputs, outputs, boundaries, dependencies, validation, and acceptance criteria explicit, but only to the level needed for the selected task profile.
- Use the smallest project structure and task profile that support the work.
- Default output language to the current conversation/window language unless the user specifies another output language.
- For code tasks involving Chinese text, names, paths, comments, or data, check encoding and CJK-related hazards before dispatch and review.

## Load As Needed

- Project scale and task profiles: `references/project-scaling.md`
- Cross-platform paired use with `serf`: `references/cross-platform-pairing.md`
- Status, dependencies, and parallelism: `references/status-and-dependencies.md`
- Dispatch modes: `references/dispatch-modes.md`
- Output language and CJK code hygiene: `references/output-language-and-cjk-code.md`
- Change control: `references/change-control.md`
- Review and acceptance: `references/review-and-acceptance.md`
- Cross-session recovery: `references/cross-session-recovery.md`
- Capability adapters:
  - `references/adapters/generic-chat-agent.md`
  - `references/adapters/coding-agent.md`
  - `references/adapters/document-agent.md`
  - `references/adapters/api-agent.md`
  - `references/adapters/shared-workspace-agent.md`
- Templates:
  - `assets/templates/project-overview.md`
  - `assets/templates/project-plan.md`
  - `assets/templates/micro-task.yaml`
  - `assets/templates/agent-task.md`
  - `assets/templates/dispatch-instruction.md`
  - `assets/templates/handoff.md`
  - `assets/templates/blocker.md`
  - `assets/templates/change-request.md`
  - `assets/templates/recovery-summary.md`
- Schemas:
  - `assets/schemas/micro-task.schema.yaml`
  - `assets/schemas/task-package.schema.yaml`
  - `assets/schemas/handoff.schema.yaml`

## Minimum Orchestration Output

For simple dispatch, include only:

- Project and task IDs.
- Task profile and task package path.
- Current status and dependencies.
- Target agent type and dispatch mode.
- Short launch instruction.

For project initialization, recovery, architecture changes, or multi-agent coordination, also include:

- Project goal, scope, and current phase.
- Selected project structure.
- Architecture and interface summary.
- Subproject mapping and execution relationships.
- Risks, blockers, and next steps.

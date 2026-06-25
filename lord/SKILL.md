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
- Select the smallest sufficient file structure from `references/project-scaling.md`.
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
6. Pick a dispatch mode from `references/dispatch-modes.md`: direct, semi-automatic, or manual copy.
7. Pick one capability adapter from `references/adapters/`. Do not create brand-specific adapters unless capability rules differ.
8. Generate task packages from `assets/templates/agent-task.md`; use schemas in `assets/schemas/` when machine-readable YAML/JSON is requested.
9. Generate launch instructions that start with `$serf` when the target platform supports skill-style invocation, then point to the formal task package instead of restating a second source of truth.
10. Process handoffs, blockers, and change requests with the templates in `assets/templates/`.
11. Adapt output language using `references/output-language-and-cjk-code.md`.
12. Review actual outputs using `references/review-and-acceptance.md`; update the authoritative state source only after review.

## Non-Negotiables

- Never claim an external agent has been started unless the current environment directly invoked it through a verified API, connector, or automation.
- Keep one authoritative state source: `TASKS.md`, `PROJECT_PLAN.md`, or `TASK_REGISTRY.yaml`, depending on project scale.
- Treat task files as requirements and handoff files as submissions; neither overrides the authoritative state source.
- Require `project_id`, `agent_id`, `task_version`, and `updated_at` in task packages.
- For Python tasks, specify the conda environment path, exact Python executable, or activation command so external agents can run the same runtime.
- Require handoffs to include `executed_task_version`; do not accept stale-version results directly.
- Make required files, inputs, outputs, boundaries, dependencies, validation, and acceptance criteria explicit for every task.
- Use the smallest project structure that supports the work.
- Default output language to the current conversation/window language unless the user specifies another output language.
- For code tasks involving Chinese text, names, paths, comments, or data, check encoding and CJK-related hazards before dispatch and review.

## Load As Needed

- Project scale and minimum structures: `references/project-scaling.md`
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
  - `assets/templates/agent-task.md`
  - `assets/templates/dispatch-instruction.md`
  - `assets/templates/handoff.md`
  - `assets/templates/blocker.md`
  - `assets/templates/change-request.md`
  - `assets/templates/recovery-summary.md`
- Schemas:
  - `assets/schemas/task-package.schema.yaml`
  - `assets/schemas/handoff.schema.yaml`

## Minimum Orchestration Output

Include at least:

- Project goal, scope, and current phase.
- Project scale and selected file structure.
- Architecture, module, and interface summary.
- Subproject letter mapping.
- Task IDs, versions, statuses, dependencies, and priorities.
- Parallel and sequential execution relationships.
- Target agent type and dispatch mode for each task.
- External agent launch instructions.
- Files to create or update.
- Current risks, blockers, and next steps.

# Task Ingestion

## 1. Required Inputs

Before execution, identify:

- `project_id`
- `agent_id`
- `task_version`
- `task_package_path`, if provided
- `authoritative_state_source`, if visible
- Required files and inputs
- Upstream dependencies and handoffs
- Allowed and forbidden controlled files
- Acceptance criteria and validation methods
- Execution environment, especially `requires_python`, `conda_env_path`, `python_executable`, and `activation_command`

## 2. Readiness Check

Proceed only when:

- Required files are readable or the task explicitly allows proceeding without them.
- The task version is the version assigned in the launch instruction or latest visible task package.
- Upstream handoffs required for this task are readable.
- The allowed work boundary is clear enough to avoid touching unrelated files.
- Validation methods are possible or a limitation can be documented.
- If Python is required, the task package or launch instruction specifies a conda environment path, exact Python executable, or activation command.

If a required input fails a readiness check, submit `BLOCKED` instead of improvising.

### Safe Assumption Rule

A safe assumption is allowed only when all are true:

- The missing information is not marked required.
- The assumption is local and reversible.
- It cannot change task scope, public interfaces, output meaning, or acceptance.
- It is recorded in the handoff `assumptions` field or section.

Otherwise submit `BLOCKED`.

## 3. Context Discipline

Read what the task requires first. Read additional files only when needed to complete or validate the assigned work. Do not use unrelated project context to expand the task scope.

## 4. Instruction Conflicts

If the launch instruction conflicts with the formal task package, follow the formal task package and report the conflict in the handoff. If the conflict changes scope, submit a blocker.

## 5. Python Runtime

When `requires_python: true`, use the specified runtime exactly:

- Prefer `python_executable` when provided.
- Otherwise use `conda_env_path` with the platform-appropriate conda invocation or activation command.
- Use `activation_command` when the task package gives one.
- Do not silently fall back to system Python or another conda environment.

If the specified runtime is unavailable, unreadable, or fails basic version checks, submit a blocker report.

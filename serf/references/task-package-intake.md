# Task Package Intake

## 1. Required Inputs

Before execution, identify:

- `project_id`
- `task_id`
- `task_version`
- `task_package_path`, if provided
- `authoritative_state_source`, if visible
- Project goal, this task's role, related task IDs, and indexed alignment files; for `micro`, derive them from `objective`, `depends_on`, and `inherits`
- Required files and inputs
- Upstream dependencies and submission reports
- Allowed and forbidden controlled files
- Acceptance criteria and validation methods
- Execution environment, especially `requires_python`, `conda_env_path`, `python_executable`, and `activation_command`

## 2. Readiness Check

Proceed only when:

- Required files are readable or the task explicitly allows proceeding without them.
- The task version matches the dispatch instruction and latest visible task package.
- Required upstream submission reports are readable.
- The planned output supports the indexed project goal and remains compatible with related tasks and interfaces.
- The allowed work boundary is clear enough to avoid touching unrelated files.
- Validation methods are possible or a limitation can be documented.
- If Python is required, the task package specifies a conda environment path, exact Python executable, or activation command.

If a required input fails a readiness check, submit `BLOCKED` instead of improvising.

### Safe Assumption Rule

A safe assumption is allowed only when all are true:

- The missing information is not marked required.
- The assumption is local and reversible.
- It cannot change task scope, public interfaces, output meaning, or acceptance.
- It is recorded in the submission report `assumptions` field or section.

Otherwise submit `BLOCKED`.

## 3. Context Discipline

Use the context index for orientation, then read only the indexed or task-required files needed to complete or validate the work. Do not use broader project visibility to expand the task scope.

## 4. Instruction Conflicts

If the dispatch instruction conflicts with the task package, follow the task package and record the conflict in the submission report. If the conflict changes scope, submit `BLOCKED`.

## 5. Python Runtime

When `requires_python: true`, use the specified runtime exactly:

- Prefer `python_executable` when provided.
- Otherwise use `conda_env_path` with the platform-appropriate conda invocation or activation command.
- Use `activation_command` when the task package gives one.
- Do not silently fall back to system Python or another conda environment.

If the specified runtime is unavailable, unreadable, or fails basic version checks, submit a blocker report.

## 6. Version Drift

The task package can move while you work.

- Re-read the package before the final report and compare `task_version` with the version you executed.
- If Lord bumped the version, submit `BLOCKED` naming both versions. A report for a version Lord no longer accepts is stale, so do not submit it as `REVIEW`.
- If the content changed but `task_version` did not, treat the package as corrupted: stop and submit `BLOCKED`.
- Never edit the task package yourself.

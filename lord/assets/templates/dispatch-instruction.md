---
project_id:
agent_id:
task_version:
target_agent_type:
dispatch_mode:
generated_at:
task_package_path:
handoff_path:
execution_environment:
  requires_python: false
  conda_env_path:
  python_executable:
  activation_command:
---

# Agent Launch Instruction

You are the external execution agent. Execute only the formal task package referenced by `task_package_path`. Do not treat this launch instruction as a second task definition.

## Read First

1. Formal task package:
2. Required files:
3. Upstream handoff files:

## Execution Requirements

- Verify `project_id`, `agent_id`, and `task_version`.
- If Python is required, use the task package's specified conda environment path, Python executable, or activation command. Do not guess a different environment.
- Work only within the allowed task boundary.
- Do not modify forbidden files.
- Record files actually read, actual changes, validation methods, and validation results.
- Submit a handoff report when complete; the status may only be `REVIEW`.
- Submit a blocker report if the task cannot continue.
- Submit a change request if public interfaces, architecture, or other task boundaries need to change.

## Python Environment

When `requires_python: true`, the launch instruction must repeat the environment values from the task package so the external agent can execute commands reproducibly.

## Return Format

Use the matching template:

- `assets/templates/handoff.md`
- `assets/templates/blocker.md`
- `assets/templates/change-request.md`

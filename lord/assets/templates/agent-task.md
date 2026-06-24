---
project_id:
agent_id:
task_version:
updated_at:
status: READY
target_agent_type:
dispatch_mode:
authoritative_state_source:
depends_on: []
execution_environment:
  requires_python: false
  conda_env_path:
  conda_env_name:
  python_executable:
  activation_command:
  package_install_policy:
---

# Task Title

## 1. Background

## 2. Objective

## 3. Required Files and Inputs

| Type | Path or source | Purpose | Required |
|---|---|---|---|

## 4. Upstream Dependencies and Handoffs

## 5. Execution Steps

## 6. Expected Outputs and Suggested Paths

| Output | Suggested path | Format | Delivered to |
|---|---|---|---|

## 7. Allowed Controlled Files

## 8. Forbidden Controlled Files

## 9. Work Boundary

### Responsible for

### Not responsible for

## 10. Acceptance Criteria

## 11. Validation Methods

## 12. Downstream Impact and Recipients

## 13. Execution Environment

For tasks that require Python, lord must specify at least one reproducible environment reference:

- `conda_env_path`, preferred when the environment exists on the target machine.
- `python_executable`, preferred when an exact interpreter path is safer.
- `activation_command`, when the target platform needs a shell-specific setup command.

If package installation is allowed, state the policy and constraints. If Python is not required, set `requires_python: false`.

## 14. Handoff Requirements

When complete, submit:

`HANDOFFS/[agent_id]-HANDOFF.md`

The handoff status may only be `REVIEW`. Do not declare `DONE`.

## 15. Blocker and Change Rules

If blocked, submit `BLOCKERS/[agent_id]-BLOCKER.md`.

If the work affects public interfaces, architecture, shared data structures, shared paths, or other tasks, submit `CHANGE_REQUESTS/[agent_id]-CHANGE-REQUEST.md` and wait for the master agent decision.

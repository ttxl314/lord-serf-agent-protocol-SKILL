---
protocol_version: "0.4"
profile: # standard | full
project_id:
task_id:
task_version:
updated_at:
task_status: READY
target_adapter:
dispatch_mode:
authoritative_state_source:
depends_on: []
submission_path: "REVIEWS/[task_id]-REVIEW.md"
execution_environment:
  requires_python: false
  conda_env_path:
  conda_env_name:
  python_executable:
  activation_command:
  package_install_policy:
---

# Task Package

## 1. Background

## 2. Objective

## 3. Inputs

| Type | Path or source | Purpose | Required |
|---|---|---|---|

## 4. Upstream Dependencies and Reports

## 5. Execution Steps

## 6. Expected Outputs

| Output | Suggested path | Format | Delivered to |
|---|---|---|---|

## 7. Allowed Paths

## 8. Forbidden Paths

## 9. Work Boundary

### Responsible for

### Not responsible for

## 10. Acceptance Criteria

Assign stable IDs such as `AC-01` to every criterion.

## 11. Validation Methods

## 12. Downstream Impact and Recipients

## 13. Execution Environment

For tasks that require Python, Lord must specify at least one reproducible environment reference:

- `conda_env_path`, preferred when the environment exists on the target machine.
- `python_executable`, preferred when an exact interpreter path is safer.
- `activation_command`, when the target platform needs a shell-specific setup command.

If package installation is allowed, state the policy and constraints. If Python is not required, set `requires_python: false`.

## 14. Submission Requirements

When complete, use `assets/templates/review-report.md` from the active Serf skill and save `REVIEWS/[task_id]-REVIEW.md`.

Set `submission_type: REVIEW`. Do not declare `DONE`.

## 15. Blocker and Change Rules

If blocked, use `assets/templates/blocker-report.md` from the active Serf skill and submit `BLOCKERS/[task_id]-BLOCKER.md`.

If the work requires a boundary, interface, architecture, shared-data, shared-path, or cross-task change, use `assets/templates/change-request-report.md`, submit `CHANGE_REQUESTS/[task_id]-CHANGE-REQUEST.md`, and wait for the Lord decision.

All template paths above are relative to the active Serf skill root.

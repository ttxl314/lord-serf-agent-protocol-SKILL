---
protocol_version: "0.6"
profile: # micro | standard | full
project_id:
task_id:
executed_task_version:
submitted_at:
submission_type: CHANGE_REQUEST
task_package_path:
report_path: "CHANGE_REQUESTS/[task_id]-CHANGE-REQUEST.md"
# Optional: application or host that executed the task.
# execution_host: dsh
---

# Change-Request Submission

## Minimal Requested Change

Describe only the smallest boundary, interface, path, architecture, or acceptance-plan change required.

## Why Current Execution Cannot Continue Safely

Explain the concrete limitation without restating the task package.

## Continuation

State whether work can continue inside the current boundary while Lord decides.

## Impact

List affected files, interfaces, tasks, rollback needs, and validation considerations only when they affect the decision.

## Decision Needed

Request `APPROVE_CHANGE`, `REJECT_CHANGE`, or `REQUEST_INFO` and identify the decision owner.

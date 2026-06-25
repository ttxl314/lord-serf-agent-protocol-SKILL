---
protocol_version: "0.3"
profile: standard
project_id:
agent_id:
executed_task_version:
submitted_at:
submission_type: CHANGE_REQUEST
task_package_path:
report_path: "CHANGE_REQUESTS/[agent_id]-CHANGE-REQUEST.md"
---

# Human Summary

1-3 short lines or bullets: the requested change, why it is required, and whether execution is blocked.

# Change Request

## Minimal Requested Change

Describe only the smallest boundary, interface, path, architecture, or acceptance-plan change required.

## Why the Current Task Cannot Continue Safely

Explain the concrete limitation without restating the full task.

## Impact

List affected files, interfaces, tasks, and rollback or validation considerations only when they affect the decision.

## Decision Needed

Request `APPROVED`, `REJECTED`, or `NEEDS_INFO` and identify the decision owner.

# Lord Change-Request Invocation

```text
$lord review CHANGE_REQUESTS/[agent_id]-CHANGE-REQUEST.md
```

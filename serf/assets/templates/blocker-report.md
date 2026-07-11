---
protocol_version: "0.4"
profile: # micro | standard | full
project_id:
task_id:
executed_task_version:
submitted_at:
submission_type: BLOCKED
task_package_path:
report_path: "BLOCKERS/[task_id]-BLOCKER.md"
---

# Blocked Submission

## Blocker

State the missing required input, permission, dependency, runtime, or decision.

## Evidence and Useful Attempts

Include only attempts that narrow the cause or prevent repeated work. Do not paste full logs.

## Needed from Lord

State the smallest input or decision required to continue.

## Reusable Work and Impact

Omit when empty. Record reusable work and affected outputs or downstream tasks.

# Lord Resolve Command

```text
$lord resolve BLOCKERS/[task_id]-BLOCKER.md
```

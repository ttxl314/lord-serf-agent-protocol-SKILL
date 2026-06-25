---
protocol_version: "0.3"
profile: standard
project_id:
agent_id:
executed_task_version:
submitted_at:
submission_type: BLOCKED
task_package_path:
report_path: "BLOCKERS/[agent_id]-BLOCKER.md"
---

# Human Summary

1-3 short lines or bullets: the critical blocker and what lord must provide or decide.

# Blocker Report

## Blocker

State the missing required input, permission, dependency, runtime, or decision.

## Evidence and Useful Attempts

Include only attempts that narrow the cause or can prevent repeated work. Do not paste full logs.

## Needed from Lord

State the smallest input or decision required to continue.

## Reusable Work and Impact

Omit when empty. Record completed reusable work and affected outputs or downstream tasks.

# Lord Blocker Invocation

```text
$lord resolve BLOCKERS/[agent_id]-BLOCKER.md
```

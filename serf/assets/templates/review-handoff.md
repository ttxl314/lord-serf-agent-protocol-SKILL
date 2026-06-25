---
protocol_version: "0.3"
profile: standard
project_id:
agent_id:
executed_task_version:
submitted_at:
submission_type: REVIEW
task_package_path:
report_path: "HANDOFFS/[agent_id]-HANDOFF.md"
---

# Human Summary

1-3 short lines or bullets: outcome, validation summary, and the item lord should inspect.

# Review Handoff

## Result

State only the completed outcome. Do not restate the task objective.

## Changed Outputs

List added, modified, or generated outputs. Mention read-only inputs only when they materially affect review.

## Acceptance Evidence

Map acceptance IDs to concise results and evidence. One check may support multiple acceptance IDs; do not duplicate logs.

## Exceptions

Omit this section when empty. Otherwise include only relevant assumptions, skipped checks, risks, incomplete items, interface impact, or a requested lord decision.

# Lord Review Invocation

```text
$lord review HANDOFFS/[agent_id]-HANDOFF.md
```

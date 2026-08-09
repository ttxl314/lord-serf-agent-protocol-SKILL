---
protocol_version: "0.5"
profile: # standard | full
project_id:
task_id:
executed_task_version:
submitted_at:
submission_type: REVIEW
task_package_path:
report_path: "REVIEWS/[task_id]-REVIEW.md"
---

# Review Submission

## Results

State only the completed outcomes. Do not restate the task objective.

## Changed Outputs

List added, modified, or generated outputs. The list may be empty for a read-only task.

## Validation Results

Map acceptance IDs to concise results and evidence. One check may support multiple acceptance IDs; do not duplicate logs.

## Exceptions

Omit this section when empty. Otherwise include only relevant assumptions, skipped checks, risks, incomplete items, interface impact, or a requested Lord decision.

# Lord Review Command

```text
$lord review REVIEWS/[task_id]-REVIEW.md
```

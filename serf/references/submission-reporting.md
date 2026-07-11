# Submission Reports

## 1. Layering

- Task package: requirements.
- Submission report: authoritative Serf evidence.
- Chat: compact notification and routing command.

Do not repeat detailed evidence in chat when it is saved in the report.

## 2. Final Response Gate

Return no more than three short content lines or bullets, excluding the command:

1. Submission type, task ID, and executed version.
2. One result, blocker, or requested change; include one concise validation result when applicable.
3. Report path.
4. One matching `$lord` command on a separate line.

## 3. REVIEW

Use `assets/templates/micro-review-report.yaml` for `micro`, or `assets/templates/review-report.md` for `standard` and `full`.

```text
REVIEW｜Task-A-01 v1
Fixed CSV blank-line parsing; 8 tests passed.
Report: REVIEWS/Task-A-01-REVIEW.yaml

$lord review REVIEWS/Task-A-01-REVIEW.yaml
```

## 4. BLOCKED

Use `assets/templates/blocker-report.md`. Record the blocker, useful attempts, smallest required Lord input, and reusable work or impact only when present.

```text
BLOCKED｜Task-A-01 v1
The specified Python runtime is unavailable.
Report: BLOCKERS/Task-A-01-BLOCKER.md

$lord resolve BLOCKERS/Task-A-01-BLOCKER.md
```

## 5. CHANGE_REQUEST

Use `assets/templates/change-request-report.md`. Record the minimal requested change, why current execution is unsafe, whether work can continue, material impact, and the needed decision.

```text
CHANGE_REQUEST｜Task-A-01 v1
A public interface change requires Lord approval.
Report: CHANGE_REQUESTS/Task-A-01-CHANGE-REQUEST.md

$lord resolve CHANGE_REQUESTS/Task-A-01-CHANGE-REQUEST.md
```

## 6. Omit Repeated Information

Do not repeat task background, acceptance text, full inventories, implementation narrative, unchanged runtime details, full commands, complete logs, or non-critical risks.

A critical unresolved risk may cause downstream failure, data loss, security exposure, invalid acceptance, or an irreversible change.

## 7. Representation and Validation

- `submission-envelope.schema.yaml` validates the common envelope and parsed Markdown front matter.
- `micro-review-report.schema.yaml` validates a completed `micro` REVIEW YAML report.
- `review-report.schema.yaml` validates a `standard` or `full` machine-readable REVIEW report.
- A report schema does not validate Markdown body structure.

## 8. Platform Cannot Save Files

Return a compact inline YAML report and state that it could not be saved:

```yaml
protocol_version: "0.4"
profile: micro
project_id: demo-project
task_id: Task-A-01
executed_task_version: "v1"
submitted_at: "2026-06-25T15:00:00-04:00"
submission_type: REVIEW
task_package_path: TASKS/Task-A-01.yaml
changed_outputs: [src/parser.py]
results: [Fixed blank-line parsing]
validation_results:
  AC-01:
    result: PASS
    evidence: "pytest tests/test_parser.py -q: 8 passed"
assumptions: []
issues: []
report_path: inline
```

If `$lord` is unsupported, replace the command with one short instruction naming the report or inline submission.

# Reporting

## 0. Human Response Principle

The report file is the authoritative submission layer. The human-facing final response is only a compact notification layer.

Detailed evidence belongs in the saved handoff, blocker, or change-request file. Do not repeat that evidence in chat.

## 1. Final Response Gate

Before sending the final response, verify that it contains:

1. Submission type, task ID, and executed task version.
2. One concise result, blocker, or change statement.
3. One concise validation result when applicable.
4. The saved report path.
5. A separate fenced `$lord` command.

Keep the human-facing content to no more than 3 short lines or 3 bullets, excluding the `$lord` command.

Do not include the full report when it has been saved successfully.

## 2. REVIEW

Use `assets/templates/micro-handoff.yaml` for small, low-risk tasks. Use `assets/templates/review-handoff.md` only when fuller evidence is needed.

The report should contain the evidence lord needs to inspect or reproduce the result. The human-facing response should contain only the outcome, validation summary, and report path.

Preferred response:

```text
REVIEW｜Agent-A-01 v1
Fixed CSV blank-line parsing; 8 tests passed.
Report: HANDOFFS/Agent-A-01.yaml

$lord review HANDOFFS/Agent-A-01.yaml
```

## 3. BLOCKED

Use `assets/templates/blocker-report.md`.

Put attempts, errors, missing inputs, and requested decisions in the blocker file. The human-facing response should state only the critical blocker and report path.

Preferred response:

```text
BLOCKED｜Agent-A-01 v1
Specified Python runtime is unavailable.
Report: BLOCKERS/Agent-A-01.yaml

$lord resolve BLOCKERS/Agent-A-01.yaml
```

## 4. CHANGE REQUEST

Use `assets/templates/change-request.md`.

Put alternatives, affected files, rollback plan, and downstream impact in the change-request file. The human-facing response should state only the essential requested change and report path.

Preferred response:

```text
CHANGE_REQUEST｜Agent-A-01 v1
Public interface change is required and has not been implemented.
Report: CHANGE_REQUESTS/Agent-A-01.yaml

$lord review CHANGE_REQUESTS/Agent-A-01.yaml
```

## 5. Information Not Repeated in Chat

When already recorded in the report file, do not repeat:

- Task background or objective recap.
- Complete file inventories.
- Implementation details.
- Runtime and environment details.
- Full commands or logs.
- Acceptance criteria text.
- Non-critical assumptions, risks, or downstream notes.
- The full report body.

Mention a risk in chat only when it is critical to the immediate human decision.

## 6. Platform Cannot Save Files

If the platform cannot create a report file:

1. State that the report could not be saved.
2. Return a compact inline YAML report.
3. Avoid a long narrative report.
4. Keep the YAML to fields needed for review.

Example:

```yaml
submission_type: REVIEW
project_id: demo-project
agent_id: Agent-A-01
executed_task_version: 1
changed:
  - src/parser.py
result:
  - Fixed blank-line parsing
validation:
  - "pytest tests/test_parser.py -q: 8 passed"
issues: []
```

## 7. Lord Invocation

Use a short path-based command:

```text
$lord review HANDOFFS/Agent-A-01.yaml
```

For blockers:

```text
$lord resolve BLOCKERS/Agent-A-01.yaml
```

For change requests:

```text
$lord review CHANGE_REQUESTS/Agent-A-01.yaml
```

If `$lord` is unsupported on the target platform, replace it with one short instruction to use the lord protocol on the named report path.

# Reporting

## 0. Layering Principle

- Task file: requirements.
- Report file: authoritative Serf submission.
- Chat: compact notification only.

Do not repeat detailed evidence in chat when it is saved in the report.

## 1. Final Response Gate

Return no more than 3 short content lines or bullets, excluding the command:

1. Submission type, task ID, and executed version.
2. One result, blocker, or requested-change statement; include one short validation result when applicable.
3. Saved report path.
4. A separate copyable `$lord` command.

Do not add a literal `# Human Summary` heading to chat unless required by the platform. That heading belongs to Markdown report templates.

## 2. REVIEW

Use `assets/templates/micro-handoff.yaml` for Micro tasks and `assets/templates/review-handoff.md` when fuller evidence is required.

The full Markdown report contains only:

- Result.
- Changed outputs.
- Acceptance evidence.
- Exceptions when present.

One validation check may support multiple acceptance IDs. Reference it once rather than duplicating logs.

```text
REVIEW｜Agent-A-01 v1
Fixed CSV blank-line parsing; 8 tests passed.
Report: HANDOFFS/Agent-A-01.yaml

$lord review HANDOFFS/Agent-A-01.yaml
```

## 3. BLOCKED

Use `assets/templates/blocker-report.md`. Include the blocker, useful evidence or attempts, the smallest needed lord input, and reusable work or impact only when present.

```text
BLOCKED｜Agent-A-01 v1
Specified Python runtime is unavailable.
Report: BLOCKERS/Agent-A-01-BLOCKER.md

$lord resolve BLOCKERS/Agent-A-01-BLOCKER.md
```

## 4. CHANGE_REQUEST

Use `assets/templates/change-request.md`. Include only the minimal requested change, why current execution cannot continue safely, material impact, and the decision needed.

```text
CHANGE_REQUEST｜Agent-A-01 v1
A public interface change is required and has not been implemented.
Report: CHANGE_REQUESTS/Agent-A-01-CHANGE-REQUEST.md

$lord review CHANGE_REQUESTS/Agent-A-01-CHANGE-REQUEST.md
```

## 5. Information Not Repeated

Do not repeat task background, objective, acceptance text, complete file inventories, implementation narrative, unchanged runtime details, full commands, full logs, or non-critical risks.

A critical unresolved risk is one that may cause downstream failure, data loss, security exposure, invalid acceptance, or an irreversible change if ignored.

## 6. Representation and Validation

- `assets/schemas/submission-envelope.schema.yaml` validates the common return envelope and parsed Markdown front matter.
- `assets/schemas/micro-handoff.schema.yaml` validates a completed Micro REVIEW YAML report.
- `assets/schemas/review-handoff.schema.yaml` validates a standard/full REVIEW YAML/JSON equivalent.
- The full review schema does not validate the Markdown body or its front matter alone.

## 7. Platform Cannot Save Files

Return a compact inline YAML report and state that it could not be saved. Do not return a long narrative.

```yaml
protocol_version: "0.3"
profile: micro
project_id: demo-project
agent_id: Agent-A-01
executed_task_version: "v1"
submitted_at: "2026-06-25T15:00:00-04:00"
submission_type: REVIEW
task_package_path: TASKS/Agent-A-01.yaml
changed: [src/parser.py]
result: [Fixed blank-line parsing]
validation:
  AC-01:
    result: PASS
    evidence: "pytest tests/test_parser.py -q: 8 passed"
assumptions: []
issues: []
report_path: inline
```

## 8. Lord Invocation

```text
$lord review HANDOFFS/Agent-A-01.yaml
$lord review HANDOFFS/Agent-A-01-HANDOFF.md
$lord resolve BLOCKERS/Agent-A-01-BLOCKER.md
$lord review CHANGE_REQUESTS/Agent-A-01-CHANGE-REQUEST.md
```

Use only the one command matching the current submission. If `$lord` is unsupported, replace it with one short instruction to use the Lord protocol on the named report path.

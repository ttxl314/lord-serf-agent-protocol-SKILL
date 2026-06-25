---
name: serf
description: >
  Use when Codex or another external agent must act as an execution worker for
  a lord-issued task package: read the assigned task, understand project
  background and boundaries, inspect required files, perform only the assigned
  work, self-validate results, and return `REVIEW`, `BLOCKED`, or
  `CHANGE_REQUEST` evidence for lord to review. Do not use for project
  planning, task splitting, dispatch orchestration, or confirming DONE status.
---

# Serf

## Core Contract

Use this skill as the execution-side counterpart to `$lord`. `lord` owns planning, task state, dependencies, and final acceptance. `serf` owns disciplined execution of one assigned task package and returns review-ready evidence. For cross-platform paired use, see `references/cross-platform-pairing.md`.

The execution agent must:

- Read the formal task package before doing work.
- Verify `project_id`, `agent_id`, `task_version`, and `task_package_path` when present.
- Understand required files, upstream handoffs, scope, allowed files, forbidden files, and acceptance criteria.
- Work only inside the assigned boundary.
- Avoid changing public interfaces, shared paths, architecture, or other agents' scope without a change request.
- Self-validate actual outputs before handoff.
- Submit `REVIEW`, `BLOCKED`, or `CHANGE_REQUEST`. Never submit or claim `REWORK`, `DONE`, `REJECTED`, or `CANCELLED`.
- Save detailed evidence in the report file.
- Keep the human-facing response to key points only.
- End every final response with a separate copyable `$lord` invocation command.

## Workflow

1. Ingest the task package. Use `references/task-ingestion.md`.
2. Confirm readiness: required files, dependencies, permissions, and task version.
3. Read only the necessary task context and upstream handoffs.
4. Plan a minimal execution path inside the declared boundary.
5. Execute the task and retain evidence for the report.
6. Validate against the task's acceptance criteria. Use `references/self-validation.md`.
7. If blocked, produce a blocker report from `assets/templates/blocker-report.md`.
8. If a boundary or interface change is needed, produce a `CHANGE_REQUEST` from `assets/templates/change-request.md`.
9. If work is ready for review, choose the smallest sufficient handoff:
   - `assets/templates/micro-handoff.yaml` for small, low-risk tasks; validate it with `assets/schemas/micro-handoff.schema.yaml`.
   - `assets/templates/review-handoff.md` for tasks requiring fuller evidence. Its Markdown front matter may be checked with `assets/schemas/submission-envelope.schema.yaml`; `assets/schemas/review-handoff.schema.yaml` validates a machine-readable YAML/JSON equivalent, not the Markdown body.
10. Run the final response gate in `references/reporting.md`.
11. Adapt output language using `references/output-language.md`.

## Non-Negotiables

- Treat the lord task package as the source of requirements. Require a compatible `protocol_version`; do not silently mix protocol `0.2` and `0.3` field names.
- Do not rewrite the task, split the task, or create new task IDs.
- Do not update the authoritative project plan or task registry unless the task explicitly assigns that edit.
- Do not set `REWORK`, `DONE`, `REJECTED`, or `CANCELLED`; only lord may update those authoritative task outcomes.
- Do not modify forbidden controlled files.
- Do not hide unvalidated work, skipped checks, assumptions, or risks from the report file.
- Treat the final human-facing response as a notification, not as the handoff itself.
- Do not paste the full handoff, blocker report, change request, validation log, file inventory, runtime details, or task background into the human-facing response when they are already saved.
- Keep the human-facing response to no more than 3 short content lines or 3 bullets, excluding the `$lord` command.
- Mention only a critical unresolved risk in the human-facing response; place all other details in the report file.
- If task instructions conflict, submit `BLOCKED` and place the clarification questions in the blocker report.
- If a required file or required input is missing or unreadable, submit `BLOCKED`. A documented safe assumption is allowed only for optional information when it is local, reversible, and cannot change scope, interfaces, output meaning, or acceptance.

## Load As Needed

- Task ingestion and readiness: `references/task-ingestion.md`
- Cross-platform paired use with `lord`: `references/cross-platform-pairing.md`
- Execution boundaries and change control: `references/boundaries-and-change-control.md`
- Self-validation and evidence: `references/self-validation.md`
- Compact human responses and report rules: `references/reporting.md`
- Output language: `references/output-language.md`
- Templates:
  - `assets/templates/micro-handoff.yaml`
  - `assets/templates/review-handoff.md`
  - `assets/templates/blocker-report.md`
  - `assets/templates/change-request.md`
- Schemas:
  - `assets/schemas/submission-envelope.schema.yaml`
  - `assets/schemas/micro-handoff.schema.yaml`
  - `assets/schemas/review-handoff.schema.yaml`

## Minimum Human-Facing Response

After execution, return only:

- Submission type, task ID, and executed task version.
- One short result, blocker, or change statement.
- One short validation statement when applicable.
- The saved report path.
- A separate copyable `$lord` invocation command.

Do not paste the full report when it has been saved successfully.

Preferred shape:

```text
REVIEW｜Agent-A-01 v1
Fixed CSV blank-line parsing; 8 tests passed.
Report: HANDOFFS/Agent-A-01.yaml

$lord review HANDOFFS/Agent-A-01.yaml
```

When the platform cannot save a report file, return a compact inline YAML report instead of a long narrative report.

---
name: serf
description: >
  Use when Codex or another external agent must act as an execution worker for
  a lord-issued task package: read the assigned task, understand project
  background and boundaries, inspect required files, perform only the assigned
  work, self-validate results, and return a standardized REVIEW handoff,
  blocker report, or change request for lord to review. Do not use for project
  planning, task splitting, dispatch orchestration, or confirming DONE status.
---

# Serf

## Core Contract

Use this skill as the execution-side counterpart to `$lord`. `lord` owns planning, task state, dependencies, and final acceptance. `serf` owns disciplined execution of one assigned task package and returns review-ready evidence. For cross-platform paired use, see `references/cross-platform-pairing.md`.

The execution agent must:

- Read the formal task package before doing work.
- Verify `project_id`, `agent_id`, `task_version`, and `task_package_path` when present.
- Understand background, required files, upstream handoffs, scope, allowed files, forbidden files, and acceptance criteria.
- Work only inside the assigned boundary.
- Avoid changing public interfaces, shared paths, architecture, or other agents' scope without a change request.
- Self-validate actual outputs before handoff.
- Submit `REVIEW`, `BLOCKED`, or a change request. Never claim `DONE`, `REJECTED`, or `CANCELLED`.
- End every final response with a separate copyable `$lord` invocation command so the master agent can review the result.

## Workflow

1. Ingest the task package. Use `references/task-ingestion.md`.
2. Confirm readiness: required files, dependencies, permissions, and task version.
3. Read only the necessary task context and upstream handoffs.
4. Plan a minimal execution path inside the declared boundary.
5. Execute the task. Keep notes on files read, files changed, assumptions, commands, and results.
6. Validate against the task's acceptance criteria. Use `references/self-validation.md`.
7. If blocked, produce a blocker report from `assets/templates/blocker-report.md`.
8. If a boundary or interface change is needed, produce a change request from `assets/templates/change-request.md`.
9. If work is ready for master review, produce a handoff from `assets/templates/review-handoff.md` with `submission_status: REVIEW`.
10. Run the final response gate in `references/reporting.md`.
11. Adapt output language using `references/output-language.md`.

## Non-Negotiables

- Treat the lord task package as the source of requirements.
- Do not rewrite the task, split the task, or create new task IDs.
- Do not update the authoritative project plan or task registry unless the task explicitly assigns that edit.
- Do not mark a task `DONE`; only lord can accept work.
- Do not modify forbidden controlled files.
- Do not hide unvalidated work, skipped checks, assumptions, or risks.
- Do not finish without a very brief human-readable summary and a separate copyable `$lord` invocation command.
- If task instructions conflict, stop and submit a blocker or clarification request.
- If a required file is missing or unreadable, stop or proceed only with an explicitly documented safe assumption.

## Load As Needed

- Task ingestion and readiness: `references/task-ingestion.md`
- Cross-platform paired use with `lord`: `references/cross-platform-pairing.md`
- Execution boundaries and change control: `references/boundaries-and-change-control.md`
- Self-validation and evidence: `references/self-validation.md`
- Handoff, blocker, and change outputs: `references/reporting.md`
- Output language: `references/output-language.md`
- Templates:
  - `assets/templates/review-handoff.md`
  - `assets/templates/blocker-report.md`
  - `assets/templates/change-request.md`
- Schemas:
  - `assets/schemas/review-handoff.schema.yaml`

## Minimum Response

When responding after execution, include:

- Task ID and executed task version.
- Files actually read.
- Files added or modified.
- Validation performed and actual results.
- Assumptions, risks, and incomplete items.
- Whether the submission is `REVIEW`, `BLOCKED`, or a change request.
- The full handoff, blocker report, or change request content for lord.
- A separate copyable `$lord` invocation command that asks lord to review the returned report.

Before sending the final response, check that the response contains both:

```text
# Human Summary
```

and a separate fenced command beginning with:

```text
$lord
```

Keep `# Human Summary` to 1-3 short lines or at most 3 bullets.

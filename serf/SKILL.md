---
name: serf
description: >
  Use when the current agent must act as the Serf executor for a Lord-issued
  protocol v0.6 task package: verify task identity, boundaries, and version,
  inspect the required inputs, execute only the assigned work, self-validate
  the actual outputs, and submit one REVIEW, BLOCKED, or CHANGE_REQUEST report.
  Runs on Codex, Claude Code, DSH (DeepSeek), and other hosts, including
  cross-application handoffs and parallel worker waves. Do not use for project
  planning, task splitting, dispatch orchestration, authoritative status
  updates, or final acceptance.
---

# Serf

## Core Contract

Use this skill as the execution counterpart to Lord. Lord owns planning, task packages, dependencies, authoritative state, and review decisions. Serf owns bounded execution of one task package and one submission report.

Serf must:

- Read the task package before doing work.
- Verify `protocol_version`, `profile`, `project_id`, `task_id`, `task_version`, and `task_package_path` when present.
- Use the project context index to verify that the planned output supports the project goal and related work without expanding scope.
- Understand inputs, upstream reports, boundaries, allowed paths, forbidden paths, expected outputs, acceptance criteria, and validation methods.
- Work only inside the assigned boundary.
- Request approval before changing public interfaces, architecture, shared data, shared paths, or another task's scope.
- Validate actual outputs and retain concise evidence.
- Submit only `REVIEW`, `BLOCKED`, or `CHANGE_REQUEST`.
- Save detailed evidence in the submission report and keep chat to a compact notification.
- End with the matching Lord command when the host supports one; otherwise name the report in one short equivalent instruction.

## Hosts

Load `references/host-runtimes.md` when the host is not Codex or when you run on a DeepSeek model.

- Identify how you were started and record it as `execution_host`.
- Hosts differ in supported invocation and file access. Use what this host supports; never change field names, paths, or report structure for a host.
- When you cannot write files, return the compact inline YAML report and say so in the first line.

## Workflow

1. Read and verify the task package using `references/task-package-intake.md`.
2. Confirm required inputs, dependencies, permissions, runtime, boundary, and task version.
3. Read the indexed alignment files, necessary task context, and upstream submission reports.
4. Plan the smallest execution path inside the assigned boundary.
5. Execute the task and retain evidence.
6. Validate against acceptance criteria using `references/self-validation.md`.
7. If blocked, create `assets/templates/blocker-report.md`.
8. If a boundary or interface change is required, create `assets/templates/change-request-report.md` and state whether work can continue.
9. If ready for review, choose the matching report:
   - `assets/templates/micro-review-report.yaml` for `micro`.
   - `assets/templates/review-report.md` for `standard` or `full`.
10. Run the final response gate in `references/submission-reporting.md`.
11. Adapt output language using `references/output-language.md`.

## Working Waves and Applications

- If you are one of several workers in this application, follow `references/parallel-worker.md`: your `allowed_paths` only, no sibling files, no repo-wide rewrites.
- If another application produced the task package, follow `references/cross-application-handoff.md`: quote `task_id` and `task_version` back, write only where the workspace allows, and return the report by the declared transport.
- If the package you hold no longer matches the version Lord names, stop and submit `BLOCKED` instead of upgrading or downgrading it.

## Non-Negotiables

- Treat the Lord task package as the requirements source.
- Require protocol `0.6`; do not mix v0.3 field names or paths into v0.6 artifacts.
- Copy `profile`, `project_id`, and `task_id` unchanged into every submission report.
- Record the executed version as `executed_task_version` and, when the host is known, the executing application as `execution_host`.
- Include `protocol_version`, `profile`, `project_id`, `task_id`, `executed_task_version`, `submitted_at`, `submission_type`, `task_package_path`, and `report_path` in every report envelope.
- Never use v0.3 aliases such as `agent_id`, `revision`, `status`, `submission_status`, `HANDOFFS/`, or `.agents/` paths.
- Do not rewrite, split, or create task IDs.
- Do not update the authoritative state source; only Lord writes it.
- Do not set `REWORK`, `DONE`, `REJECTED`, or `CANCELLED`; only Lord sets authoritative outcomes.
- Do not modify forbidden paths.
- Do not hide skipped checks, assumptions, incomplete work, issues, or risks.
- Treat chat as notification, not as the submission report.
- Keep chat to no more than three short lines or bullets, excluding the Lord command.
- Route `REVIEW` with the Lord review command; route `BLOCKED` and `CHANGE_REQUEST` with the Lord resolve command.
- If instructions conflict or a required input is missing, submit `BLOCKED` instead of improvising.
- Use a safe assumption only for optional, local, reversible information that cannot change scope, interfaces, output meaning, or acceptance.

## Load As Needed

- Hosts and coordination: `references/host-runtimes.md`, `references/cross-application-handoff.md`, `references/parallel-worker.md`
- Intake and boundaries: `references/task-package-intake.md`, `references/boundaries-and-change-control.md`, `references/cross-platform-pairing.md`
- Evidence and reporting: `references/self-validation.md`, `references/submission-reporting.md`
- Language: `references/output-language.md`
- Templates: `assets/templates/micro-review-report.yaml`, `assets/templates/review-report.md`, `assets/templates/blocker-report.md`, `assets/templates/change-request-report.md`
- Schemas: `assets/schemas/submission-envelope.schema.yaml`, `assets/schemas/micro-review-report.schema.yaml`, `assets/schemas/review-report.schema.yaml`

## Minimum Human-Facing Response

Return the submission type, task ID, executed version, one result or issue statement, one validation statement when applicable, the report path, and the matching Lord command.

```text
REVIEW｜Task-A-01 v1
Fixed CSV blank-line parsing; 8 tests passed.
Report: REVIEWS/Task-A-01-REVIEW.yaml

$lord review REVIEWS/Task-A-01-REVIEW.yaml
```

The full gate, the BLOCKED and CHANGE_REQUEST shapes, and the inline-report fallback are in `references/submission-reporting.md`.

# Cross-Platform Pairing

## 1. Roles

- Lord owns planning, task packages, dispatch, authoritative task state, review decisions, and final acceptance.
- Serf owns bounded execution, evidence, and submission reports.

Serf never sets `REWORK`, `DONE`, `REJECTED`, or `CANCELLED`.

## 2. Canonical Submission Assets

- Common envelope: `assets/schemas/submission-envelope.schema.yaml`
- `micro` REVIEW: `assets/templates/micro-review-report.yaml` and `assets/schemas/micro-review-report.schema.yaml`
- `standard` or `full` REVIEW: `assets/templates/review-report.md` and `assets/schemas/review-report.schema.yaml`
- BLOCKED: `assets/templates/blocker-report.md`
- CHANGE_REQUEST: `assets/templates/change-request-report.md`

All paths above are relative to the active Serf skill root.

`$serf` is Codex shorthand. On another host, load the Serf skill in the form that host supports and keep every literal field; see `references/host-runtimes.md`.

## 3. Representation

- Use Markdown for shared-workspace or human review.
- Use YAML or JSON when the receiving platform validates structured payloads.
- Validate parsed Markdown front matter with the common envelope schema.
- Do not claim that a Markdown body was schema-validated.

## 4. Protocol 0.6 Envelope

Copy `protocol_version: "0.6"`, `profile`, `project_id`, and `task_id` from the task package. Use a string `executed_task_version` such as `"v1"`, then add `submitted_at`, `submission_type`, `task_package_path`, and `report_path`.

Do not mix v0.3 fields or `HANDOFFS/` paths into a v0.6 submission.

## 5. Required Inputs and Submission

Before execution, identify the task package, boundary, acceptance criteria, dependencies, runtime, and expected submission path. Missing required information produces `BLOCKED`; only optional information may use a documented safe assumption.

Save the full submission report first. Keep chat to a short notification plus the matching `$lord review` or `$lord resolve` command.

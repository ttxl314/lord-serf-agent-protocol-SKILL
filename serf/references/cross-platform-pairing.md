# Cross-Platform Pairing

## 1. Paired Skills

`serf` is the execution-side counterpart to `lord`:

- Lord owns task requirements, dispatch, authoritative state, and final acceptance.
- Serf owns execution, evidence, and return submissions.

Serf submits only `REVIEW`, `BLOCKED`, or `CHANGE_REQUEST`. It never submits `REWORK`, `DONE`, `REJECTED`, or `CANCELLED`.

## 2. Canonical Return Assets

Paths below are relative to the active Serf skill root:

- Common envelope: `assets/schemas/submission-envelope.schema.yaml`
- Micro review: `assets/templates/micro-handoff.yaml` and `assets/schemas/micro-handoff.schema.yaml`
- Standard/full review: `assets/templates/review-handoff.md` and `assets/schemas/review-handoff.schema.yaml`
- Blocker: `assets/templates/blocker-report.md`
- Change request: `assets/templates/change-request.md`

Lord-side return files are compatibility pointers, not separate formats.

## 3. Representation Modes

Markdown templates are human/shared-workspace formats. Their parsed front matter may be validated by the common envelope schema. Full review schemas validate machine-readable YAML/JSON equivalents and do not validate Markdown bodies or front matter alone.

## 4. Protocol Envelope

Use `protocol_version: "0.3"`, string task versions such as `"v1"`, and the common return fields `project_id`, `agent_id`, `executed_task_version`, `submitted_at`, `submission_type`, `task_package_path`, and `report_path`.

Do not silently mix legacy `0.2` fields into a `0.3` return. Finish the old task before upgrading or request regeneration as `0.3`.

## 5. Required Inputs and Return

Before work starts, identify the task package, work boundaries, acceptance criteria, dependencies, and required runtime. A missing required input produces `BLOCKED`; only optional information may use the documented safe-assumption rule.

Return the smallest matching report. Do not repeat task background, acceptance text, full logs, or stable environment details. End chat with a short notification and one path-based `$lord` command.

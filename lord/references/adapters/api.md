# API Adapter

## Dispatch

- Include `protocol_version`, `profile`, `project_id`, `task_id`, string task version, and an idempotency key.
- Define authentication, endpoint, timeout, retry, and rate-limit behavior.
- Keep the task package as the requirements source; do not embed a divergent second task definition.
- Record the remote invocation ID only as transport metadata.

## Submission Contract

Require:

- `protocol_version`
- `profile`
- `project_id`
- `task_id`
- `executed_task_version`
- `submitted_at`
- `submission_type`
- `task_package_path`
- `report_path`

Validate common fields with the active Serf skill's `assets/schemas/submission-envelope.schema.yaml`. A submission type is not a task status, and an error response is not a successful submission.

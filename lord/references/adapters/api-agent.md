# API Agent Adapter

Use for agents invoked through an API, workflow platform, or automation orchestrator.

## Dispatch Requirements

- Use JSON or YAML.
- Include `protocol_version`, project ID, agent ID, string task version, and an idempotency key.
- Define input references, output locations, timeout behavior, and error semantics.
- Do not claim start or completion until a verifiable success response is received.

## Return Contract

Validate the common fields with the active Serf skill's `assets/schemas/submission-envelope.schema.yaml`.

Recommended fields:

- `protocol_version`
- `project_id`
- `agent_id`
- `executed_task_version`
- `submitted_at`
- `submission_type`
- `task_package_path`
- `report_path` or `report_content`
- `result`, `validation`, and material exceptions when applicable

`submission_type` is not task status. Lord updates the authoritative task status after review. Do not present an error response as a successful return.

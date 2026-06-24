# API Agent Adapter

Use for agents invoked through an API, workflow platform, or automation orchestrator.

## Dispatch Requirements

- Use JSON or YAML.
- Fields must be explicit and not depend on implicit context.
- Include project ID, task ID, task version, and an idempotency key.
- Define input file references, output locations, timeout behavior, and error semantics.
- Map returned statuses to standard task statuses.
- Do not present an error response as a successful handoff.
- Do not claim the external agent has started or completed until a verifiable success response is received.

## Recommended Return Fields

- `project_id`
- `agent_id`
- `executed_task_version`
- `submission_status`
- `outputs`
- `validation`
- `assumptions`
- `risks`
- `blockers`
- `handoff_content`

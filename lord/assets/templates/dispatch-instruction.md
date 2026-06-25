---
protocol_version: "0.3"
project_id:
agent_id:
task_version:
target_agent_type:
dispatch_mode:
generated_at:
task_package_path:
handoff_path:
worker_skill: serf
worker_invocation: "$serf"
execution_environment:
  requires_python: false
  conda_env_path:
  python_executable:
  activation_command:
---

# Agent Launch Instruction

## Invocation Header

If the target platform supports skill invocation, start with:

```text
$serf
```

If `$serf` is unsupported, load the active Serf skill instruction once for the independent session. Do not resend the full skill or references on later tasks unless the protocol version changes.

Execute only the formal task package at `task_package_path`. This launch instruction is not a second task definition.

## Read First

1. Formal task package:
2. Required files not already referenced by the task:
3. Required upstream handoffs:

## Execution Requirements

- Verify `protocol_version`, `project_id`, `agent_id`, and `task_version`.
- Use the task-defined runtime; do not guess a different environment.
- Stay inside the declared boundary and do not modify forbidden files.
- Save detailed evidence in the return file.
- End with a brief human-facing notification of 1-3 lines or bullets, followed by a separate copyable `$lord` command. Do not add a literal `# Human Summary` heading to chat unless the platform requires one.
- Return only `submission_type: REVIEW`, `BLOCKED`, or `CHANGE_REQUEST`.

## Return Format

Use the matching canonical asset from the active Serf skill:

- Micro `REVIEW`: `assets/templates/micro-handoff.yaml`
- Standard/full `REVIEW`: `assets/templates/review-handoff.md`
- `BLOCKED`: `assets/templates/blocker-report.md`
- `CHANGE_REQUEST`: `assets/templates/change-request.md`

Path base: the paths above are relative to the active Serf skill root. In a sibling offline installation, the Serf root is commonly `../serf/` relative to the Lord skill root. Do not use Lord compatibility pointers as return payloads.

---
protocol_version: "0.6"
profile: # micro | standard | full
project_id:
task_id:
task_version:
target_adapter:
dispatch_mode:
generated_at:
task_package_path:
submission_path:
worker_skill: serf
worker_invocation: "$serf"  # host form, for example 'skill("serf")' on DSH
# Optional host block: record the application and model that will execute the task.
# host:
#   agent: dsh
#   model: deepseek-flash
#   skill_invocation: 'skill("serf")'
#   supports_subagents: true
#   shared_workspace: true
# Optional handoff block: only when the executor runs in another application.
# handoff:
#   from_app: dsh
#   to_app: word
#   transport: upload
#   return_transport: upload
---

# Serf Launch Instruction

## Invocation

Invoke the Serf skill in the form this host supports:

- Codex: `$serf`
- Claude Code: `/serf` or the skill name
- DSH: `skill("serf")`, usually through a subagent
- Any other host: load `SKILL.md` once in the independent session

Do not resend the skill or its references unless the protocol version changes.

Execute only the task package at `task_package_path`. This launch instruction is not a second task definition.

## Read First

1. Task package.
2. Required inputs not already referenced by the task package.
3. Required upstream submission reports.

## Execution Requirements

- Verify `protocol_version`, `profile`, `project_id`, `task_id`, and `task_version`.
- Use the runtime defined by the task package.
- Stay inside the declared boundary and do not modify forbidden paths.
- Record the executing host as `execution_host` when the report format allows it.
- Save detailed evidence in the submission report.
- Keep chat to 1-3 short lines or bullets plus the matching Lord command.
- Submit only `REVIEW`, `BLOCKED`, or `CHANGE_REQUEST`.

## Submission Format

Use the matching asset from the active Serf skill:

- `micro` `REVIEW`: `assets/templates/micro-review-report.yaml`
- `standard` or `full` `REVIEW`: `assets/templates/review-report.md`
- `BLOCKED`: `assets/templates/blocker-report.md`
- `CHANGE_REQUEST`: `assets/templates/change-request-report.md`

These paths are relative to the active Serf skill root.

# Cross-Platform Pairing

## 1. Paired Skills

`lord` and `serf` are one paired protocol:

- `lord`: planning, task packages, dispatch, authoritative state, and final acceptance.
- `serf`: bounded execution, self-validation, and return submissions.

Serf submits only `REVIEW`, `BLOCKED`, or `CHANGE_REQUEST`. Lord alone may set authoritative outcomes such as `REWORK`, `DONE`, `REJECTED`, or `CANCELLED`.

## 2. Authority Map

- Task requirements and task schemas are owned by Lord.
- Return templates and return schemas are owned by Serf.
- Lord-side `handoff.md`, `blocker.md`, and `change-request.md` are compatibility pointers only.
- The project plan or task registry is the only authoritative task-status source.

Do not maintain a second copy of a Serf return contract inside Lord.

## 3. Path Base

Paths shown as `assets/...` in return instructions are relative to the active Serf skill root. In a sibling offline installation such as `.codex/skills/lord` and `.codex/skills/serf`, the Serf root is commonly `../serf/` relative to Lord. In platforms with skill discovery, prefer the logical form `active Serf skill → assets/...` instead of hard-coding a filesystem path.

## 4. Protocol Envelope

Protocol `0.3` uses string task versions and the common return fields `protocol_version`, `project_id`, `agent_id`, `executed_task_version`, `submitted_at`, `submission_type`, `task_package_path`, and `report_path`.

Do not silently combine protocol `0.2` fields such as `submission_status`, `status: BLOCKED`, or `change_status` with protocol `0.3` returns. Finish an active `0.2` task before upgrading, or regenerate it as `0.3`.

## 5. Representation Modes

- Markdown templates are human/shared-workspace formats.
- Machine schemas validate YAML/JSON equivalents.
- `submission-envelope.schema.yaml` may validate parsed Markdown front matter.
- A full machine schema does not validate a Markdown body or front matter alone.

## 6. Dispatch Handshake

Dispatch only the Serf invocation, formal task package path, required unavailable inputs, and essential runtime note. Do not repeat task goals, boundaries, acceptance text, or stable context already available by reference.

A Serf return contains one canonical report path, concise evidence, and one short path-based `$lord` command. Chat is notification only.

## 7. Non-Codex Naming

Where `$lord` and `$serf` are unsupported, call them the Lord orchestration protocol and Serf execution protocol. The names are handles; file contracts remain authoritative.

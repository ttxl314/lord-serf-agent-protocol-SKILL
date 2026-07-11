# Cross-Platform Pairing

## 1. Roles

- Lord owns planning, task packages, dispatch, authoritative task state, review decisions, and final acceptance.
- Serf owns bounded execution, self-validation, and one submission report per task execution.

Serf submits only `REVIEW`, `BLOCKED`, or `CHANGE_REQUEST`. Lord alone sets authoritative outcomes.

## 2. Asset Ownership

- Lord owns task-package and dispatch assets.
- Serf owns submission templates and schemas.
- Do not duplicate the Serf submission contract inside the Lord skill.

Paths beginning with `assets/` are relative to the active skill root. In a sibling offline installation, the Serf root is commonly `../serf/` relative to Lord.

## 3. Protocol 0.4 Envelope

Use string task versions and these common submission fields:

- `protocol_version`
- `profile`
- `project_id`
- `task_id`
- `executed_task_version`
- `submitted_at`
- `submission_type`
- `task_package_path`
- `report_path`

Do not mix v0.3 fields such as `agent_id`, `status`, `return_path`, `handoff_path`, `changed`, `result`, or `validation` into v0.4 artifacts.

## 4. Representation

- Markdown templates are the shared-workspace and human-review format.
- YAML or JSON schemas validate machine-readable equivalents.
- `submission-envelope.schema.yaml` validates parsed Markdown front matter.
- Schema validation does not validate Markdown body structure.

## 5. Dispatch Handshake

Dispatch only the Serf invocation, task-package path, unavailable required inputs, and essential runtime note. Do not repeat goals, boundaries, acceptance text, or stable context already stored in the task package.

Every Serf submission contains one report path, concise evidence, and one matching path-based `$lord` command in chat. The command is transport metadata, not a machine-report field.

## 6. Non-Codex Platforms

Treat `lord` and `serf` as role names when skill invocation is unavailable. Preserve protocol field names, status values, submission types, adapter names, and paths exactly.

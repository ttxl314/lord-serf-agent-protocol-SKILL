# Cross-Platform Pairing

## 1. Paired Skills

`lord` and `serf` are a paired protocol:

- `lord`: master planner, task splitter, dispatcher, state owner, and final reviewer.
- `serf`: external execution worker that reads one lord task package, performs bounded work, self-validates, and returns `REVIEW`, `BLOCKED`, or a change request.

Use `lord` for the controlling agent and `serf` for each external or independent execution agent.

## 2. Portable Bundle

When moving this pair to another platform, carry:

- `lord/SKILL.md`
- `lord/references/`
- `lord/assets/templates/`
- `lord/assets/schemas/`
- `serf/SKILL.md`
- `serf/references/`
- `serf/assets/templates/`
- `serf/assets/schemas/`

`agents/openai.yaml` is optional UI metadata for Codex-like environments. It is not required for the protocol.

## 3. Platforms Without Skill Support

If the target platform does not support Codex skills:

- Use `lord/SKILL.md` as the master agent's system or project instruction.
- Use `serf/SKILL.md` as the external agent's system or project instruction.
- Provide referenced files as attachments, project files, or pasted context.
- Keep templates available to both sides.
- Preserve literal IDs, paths, statuses, and schema keys.

## 4. Dispatch Handshake

Every lord-to-serf dispatch should include:

- Invocation header `$serf` when the target platform supports skill-style invocation.
- If `$serf` is unsupported, the content of `serf/SKILL.md` or an equivalent execution-worker instruction.
- Formal task package, preferably from `lord/assets/templates/agent-task.md`.
- Launch instruction, preferably from `lord/assets/templates/dispatch-instruction.md`.
- Required files and upstream handoffs.
- Expected return template path or pasted template.
- Python/conda runtime details when Python execution is needed.

Every serf-to-lord return should include:

- `executed_task_version`
- files actually read
- files added or modified
- validation methods and actual results
- runtime used for Python work
- assumptions, risks, and incomplete items
- `submission_status: REVIEW`, `status: BLOCKED`, or a change request

## 5. Non-Codex Naming

In platforms where `$lord` and `$serf` are not supported, refer to them as:

- Lord protocol: master orchestration instructions.
- Serf protocol: external execution-worker instructions.

The names are convenience handles, not platform dependencies.

When generating a manual-copy dispatch, lord should still include `$serf` as the first line for platforms that can use it, followed by a fallback note for platforms that cannot.

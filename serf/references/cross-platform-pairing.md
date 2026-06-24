# Cross-Platform Pairing

## 1. Paired Skills

`serf` is the execution-side counterpart to `lord`:

- `lord` creates the task package, launch instruction, environment requirements, dependencies, and acceptance criteria.
- `serf` reads the task package, executes only the assigned work, validates outputs, and returns a review-ready report.

Do not use `serf` as a planner or dispatcher. Do not confirm `DONE`; lord owns final acceptance.

## 2. Portable Bundle

When moving this pair to another platform, carry:

- `serf/SKILL.md`
- `serf/references/`
- `serf/assets/templates/`
- `serf/assets/schemas/`
- the lord task package and launch instruction
- any required files and upstream handoffs

If the external platform can also access the lord skill package, provide `lord/SKILL.md`, `lord/references/`, and `lord/assets/` as protocol reference material.

`agents/openai.yaml` is optional UI metadata for Codex-like environments. It is not required for execution.

## 3. Platforms Without Skill Support

If the target platform does not support Codex skills:

- Use `serf/SKILL.md` as the external agent's system or project instruction.
- Attach or paste the required `serf/references/` files when needed.
- Attach or paste the relevant return template.
- Treat the lord task package as the source of requirements.
- Keep status values, IDs, file paths, schema keys, and commands literal.

## 4. Required Dispatch Inputs

Before work starts, serf should receive:

- `project_id`
- `agent_id`
- `task_version`
- task package
- launch instruction, if any
- required files and upstream handoffs
- allowed and forbidden file boundaries
- acceptance criteria and validation methods
- Python/conda runtime details when Python execution is needed

If these are missing and cannot be safely inferred from the task package, return a blocker report.

## 5. Required Return to Lord

Return one of:

- Review handoff from `assets/templates/review-handoff.md`.
- Blocker report from `assets/templates/blocker-report.md`.
- Change request from `assets/templates/change-request.md`.

Never return `DONE`. Use `REVIEW` when ready for lord to inspect.

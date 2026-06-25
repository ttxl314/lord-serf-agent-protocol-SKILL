# Lord and Serf

[![中文](https://img.shields.io/badge/语言-中文-red)](README.zh-CN.md)

Cross-platform paired agent skills for file-based multi-agent project orchestration.

- `lord` is the master orchestration skill. It plans work, creates bounded task packages, controls authoritative task state, and performs final acceptance.
- `serf` is the execution-worker skill. It executes one lord-issued task package, self-validates the result, and submits `REVIEW`, `BLOCKED`, or `CHANGE_REQUEST` evidence.

## Protocol at a Glance

- Current protocol version: `0.3`.
- Project state is stored in files rather than chat memory.
- Task profiles are `micro`, `standard`, and `full`.
- Lord owns requirements and authoritative status; Serf owns return templates and return schemas.
- Only Lord may set `REWORK`, `DONE`, `REJECTED`, or `CANCELLED`.
- Human-facing chat is a short notification. Detailed evidence belongs in the saved report file.

## Why This Exists

Many agent workflows span multiple tools, platforms, repositories, or independent sessions. Chat history alone is not a reliable project-state system. `lord` and `serf` define a portable protocol based on Markdown, YAML, templates, schemas, stable IDs, and file paths so that planning, execution, review, and recovery remain reproducible across environments.

## Repository Structure

```text
.
├── lord/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/
│   │   ├── schemas/
│   │   └── templates/
│   └── references/
└── serf/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── assets/
    │   ├── schemas/
    │   └── templates/
    └── references/
```

Key ownership rule:

```text
lord/assets/...  = task and dispatch assets
serf/assets/...  = execution return assets
```

Within an active Skill, `assets/...` paths are relative to that Skill's root.

## Install in Codex

Copy both folders into the Codex skills directory. A common layout is:

```text
~/.codex/skills/lord
~/.codex/skills/serf
```

The files should be directly available as:

```text
~/.codex/skills/lord/SKILL.md
~/.codex/skills/serf/SKILL.md
```

This can be a fully offline copy. No repository link, symbolic link, or automatic synchronization is required. Restart Codex after replacing an installed version.

Invoke the skills as:

```text
$lord
$serf
```

`agents/openai.yaml` is Codex-oriented UI metadata. It is useful for Codex-like environments but not required for the underlying protocol.

## Cross-Platform Use

These skills are not tightly bound to Codex.

1. Use `lord/SKILL.md` as the master-agent instruction.
2. Use `serf/SKILL.md` as the execution-worker instruction.
3. Load each Skill once per independent software session when possible.
4. In a shared workspace, dispatch later tasks by task-package path instead of repeating the complete protocol.
5. Without a shared workspace, transfer only the task package, required inputs, and the matching Serf return template.
6. Preserve literal IDs, statuses, schema keys, command names, and report paths.

## Task Profiles

| Profile | Use when | Typical return |
|---|---|---|
| `micro` | One low-risk, isolated objective with at most three acceptance criteria | Compact YAML handoff |
| `standard` | Ordinary module-level work with related files and routine validation | Compact Markdown or machine-readable handoff |
| `full` | Architecture, shared schema, complex dependencies, security, migration, or difficult rollback | Fuller evidence with risk-focused review |

Use the smallest profile that can execute the work safely.

## Core Workflow

1. `lord` selects the smallest sufficient project structure and task profile.
2. `lord` creates IDs such as `Agent-A-01` and writes the formal task package.
3. `lord` defines the objective, boundaries, dependencies, expected outputs, acceptance IDs, validation, and runtime requirements.
4. `serf` reads the task package and performs only the assigned work.
5. `serf` self-validates and submits `REVIEW`, `BLOCKED`, or `CHANGE_REQUEST`.
6. `lord` inspects the actual outputs, applies risk-based review, and updates the authoritative state source.

## Return Contract

All Serf returns share this envelope:

```yaml
protocol_version: "0.3"
project_id:
agent_id:
executed_task_version:
submitted_at:
submission_type: REVIEW  # REVIEW | BLOCKED | CHANGE_REQUEST
task_package_path:
report_path:
```

Canonical return assets are under the active Serf Skill:

```text
assets/templates/micro-handoff.yaml
assets/templates/review-handoff.md
assets/templates/blocker-report.md
assets/templates/change-request.md
assets/schemas/submission-envelope.schema.yaml
assets/schemas/micro-handoff.schema.yaml
assets/schemas/review-handoff.schema.yaml
```

Markdown templates are human/shared-workspace formats. Full task and review schemas validate machine-readable YAML or JSON equivalents; they do not validate a Markdown body by themselves.

## Report Paths and Commands

```text
Micro review:       HANDOFFS/Agent-A-01.yaml
Full review:        HANDOFFS/Agent-A-01-HANDOFF.md
Blocker:            BLOCKERS/Agent-A-01-BLOCKER.md
Change request:     CHANGE_REQUESTS/Agent-A-01-CHANGE-REQUEST.md
```

```text
$lord review HANDOFFS/Agent-A-01.yaml
$lord review HANDOFFS/Agent-A-01-HANDOFF.md
$lord resolve BLOCKERS/Agent-A-01-BLOCKER.md
$lord review CHANGE_REQUESTS/Agent-A-01-CHANGE-REQUEST.md
```

## Context and Review Economy

- Reference authoritative project files instead of repeating stable context.
- Keep launch instructions to a task path and essential execution note.
- Map evidence to stable acceptance IDs.
- One validation command may support multiple acceptance criteria.
- Micro review normally reuses Serf evidence after inspecting the actual output.
- Standard review reproduces uncertain, representative, or high-value checks.
- Full review reproduces critical high-risk checks.
- Rework instructions contain only the failed or affected criteria, required changes, preserved behavior, and checks that must be rerun.

## Python and Conda Runtime Handoff

For Python tasks, `lord` should specify one or more of:

- `conda_env_path`
- `conda_env_name`
- `python_executable`
- `activation_command`
- `package_install_policy`

`serf` must use the specified runtime and record the runtime actually used. If the runtime is unavailable, `serf` should return `BLOCKED` instead of silently falling back to another interpreter.

## Language and CJK Safety

The skills are written in English for cross-platform model efficiency. They also include guidance for Chinese and CJK text in code work, including UTF-8 encoding, full-width punctuation, non-ASCII paths, shell quoting, Unicode-aware checks, and rendering-width issues.

## Validation

If you have Codex's `skill-creator` validator available:

```powershell
python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ".\lord"
python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ".\serf"
```

Expected result:

```text
Skill is valid!
```

## Migrating from Protocol 0.2

Complete active `0.2` tasks before replacing the installed Skills, or regenerate unfinished task packages as `0.3`. Do not mix `0.2` and `0.3` return fields in the same task or report.

## Star History

<p align="center">
  <a href="https://www.star-history.com/#ttxl314/lord-serf-agent-protocol-SKILL&Date">
    <picture>
      <source
        media="(prefers-color-scheme: dark)"
        srcset="https://api.star-history.com/chart?repos=ttxl314/lord-serf-agent-protocol-SKILL&type=date&theme=dark&legend=top-left"
      />
      <source
        media="(prefers-color-scheme: light)"
        srcset="https://api.star-history.com/chart?repos=ttxl314/lord-serf-agent-protocol-SKILL&type=date&legend=top-left"
      />
      <img
        alt="Star History Chart"
        src="https://api.star-history.com/chart?repos=ttxl314/lord-serf-agent-protocol-SKILL&type=date&legend=top-left"
      />
    </picture>
  </a>
</p>


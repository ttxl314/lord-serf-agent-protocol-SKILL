# Lord and Serf

[![English](https://img.shields.io/badge/Language-English-blue)](README.md)

Cross-platform paired agent skills for multi-agent project orchestration.

- `lord` is the master orchestration skill. It plans complex work, splits projects into external-agent task packages, defines boundaries and acceptance criteria, dispatches work, and owns final review.
- `serf` is the execution-worker skill. It receives a lord-issued task package, reads the required context, performs only the assigned work, self-validates, and returns a review-ready handoff, blocker report, or change request.

Chinese version: [README.zh-CN.md](README.zh-CN.md)

## Why This Exists

Many agent workflows span multiple tools, platforms, or independent sessions. Chat history alone is not a reliable project state system. `lord` and `serf` define a portable protocol based on Markdown, YAML, templates, and schemas so that a master agent and external execution agents can collaborate without relying on a single vendor or runtime.

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

## Use in Codex

Install both folders into your Codex skills directory:

```text
~/.codex/skills/lord
~/.codex/skills/serf
```

Then invoke them as:

```text
$lord
$serf
```

`agents/openai.yaml` is Codex-oriented UI metadata. It is useful for Codex-like environments but not required for the underlying protocol.

## Cross-Platform Use

These skills are not tightly bound to Codex. For another platform:

1. Use `lord/SKILL.md` as the master agent system or project instruction.
2. Use `serf/SKILL.md` as the execution-worker system or project instruction.
3. Provide relevant files from `references/` as needed.
4. Provide templates from `assets/templates/` for task packages, handoffs, blockers, and change requests.
5. Use schemas from `assets/schemas/` when structured YAML or JSON validation is useful.

Keep literal values unchanged across platforms: task IDs, status values, file paths, schema keys, command names, and runtime paths.

## Core Workflow

1. `lord` analyzes the project and selects the smallest sufficient project structure.
2. `lord` creates task IDs such as `Agent-A-01` and writes formal task packages.
3. `lord` defines required files, boundaries, dependencies, validation, expected outputs, and Python/conda runtime details when needed.
4. `serf` receives a task package and executes only the assigned task.
5. `serf` self-validates and returns `REVIEW`, `BLOCKED`, or a change request.
6. `lord` reviews actual outputs and is the only side that may confirm `DONE`.

## Python and Conda Runtime Handoff

For Python tasks, `lord` should specify one or more of:

- `conda_env_path`
- `conda_env_name`
- `python_executable`
- `activation_command`
- `package_install_policy`

`serf` must use the specified runtime and record the runtime actually used in the handoff. If the specified runtime is unavailable, `serf` should return a blocker instead of silently falling back to system Python.

## Language and CJK Safety

The skills are written in English for cross-platform model efficiency. They also include guidance for Chinese and CJK text in code work, including UTF-8 encoding, full-width punctuation, non-ASCII paths, shell quoting, Unicode-aware checks, and rendering width issues.

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

## Recommended GitHub Contents

Commit:

- `lord/`
- `serf/`
- `README.md`
- `README.zh-CN.md`
- `.gitignore`

You usually do not need to commit old zip exports or local temporary files.

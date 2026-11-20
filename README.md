# Lord and Serf

[![中文](https://img.shields.io/badge/语言-中文-red)](README.zh-CN.md)

Cross-platform paired skills for file-based orchestration of complex multi-executor projects.

- `lord` is the orchestration skill. It plans work, creates task packages, dispatches Serf executors, controls authoritative task state, and makes review decisions.
- `serf` is the execution skill. It executes one Lord-issued task package, validates actual outputs, and creates one submission report.

## Protocol 0.6

The canonical lifecycle is:

```text
plan → package → dispatch → execute → submit → review → decide
```

Use these terms consistently:

| Concept | Canonical name |
|---|---|
| Orchestration role | Lord |
| Execution role | Serf |
| Requirements artifact | Task package |
| Start instruction | Dispatch instruction |
| Execution evidence | Submission report |
| Project status authority | Authoritative state source |
| Stable work identifier | `Task-A-01` style task ID |

Chat is notification only. Project state, requirements, evidence, and decisions belong in files.

Protocol 0.6 makes the two coordination patterns below first-class: optional `host` and `handoff` dispatch blocks, optional `execution_host` in reports, rules for duplicate submissions and in-flight version changes, and host documentation for Claude Code, Codex, and DSH. Field names are unchanged from 0.5; the only incompatible change is the `protocol_version` constant.

## Repository Structure

```text
.
├── .editorconfig
├── .gitattributes
├── .github/workflows/validate.yml
├── CHANGELOG.md
├── lord/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/{schemas,templates}/
│   └── references/
├── serf/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/{schemas,templates}/
│   └── references/
├── scripts/validate_repo.py
└── requirements-dev.txt
```

Lord owns task and dispatch assets. Serf owns submission assets. Paths under `assets/` are relative to the active skill root.

## Install

| Host | Skill directory | Invoke | Start an executor |
|---|---|---|---|
| Codex | `~/.codex/skills/lord`, `~/.codex/skills/serf` | `$lord`, `$serf` | multi-agent subagents where enabled |
| Claude Code | `~/.claude/skills/lord`, `~/.claude/skills/serf` | `/lord`, `/serf`, or automatic | `Task` subagents |
| DSH (DeepSeek) | `~/.dsh/skills/lord`, `~/.dsh/skills/serf` | `skill("lord")`, `skill("serf")` | `subagent` or `subagent_fork` |
| Generic chat | attach the two `SKILL.md` files | none | human copy |

Copy both folders, reload the host, then invoke. Project-local installs also work: `.codex/skills/` for Codex and `.claude/skills/` for Claude Code.

`$lord` and `$serf` are Codex shorthand. On any other host, use that host's invocation and keep every literal field. `agents/openai.yaml` is Codex UI metadata and is ignored elsewhere; DSH reads only the `SKILL.md` front matter.

Host limits worth knowing before you dispatch: Claude Code writes may wait on approval, Codex writes are bound by its sandbox policy, and DSH writes are workspace-scoped. A blocked write is a blocker, never a reason to move the output. Details: `lord/references/host-runtimes.md`.

## Task Profiles

| Profile | Use when | REVIEW report |
|---|---|---|
| `micro` | One low-risk isolated objective with at most three acceptance criteria | Compact YAML |
| `standard` | Ordinary module-level work with routine validation | Markdown or machine-readable equivalent |
| `full` | Architecture, shared schemas, complex dependencies, security, migration, or difficult rollback | Risk-focused Markdown or machine-readable equivalent |

Use the smallest profile that can execute the work safely.

## Protocol Namespaces

| Namespace | Values |
|---|---|
| `task_status` | `PENDING`, `READY`, `IN_PROGRESS`, `BLOCKED`, `REVIEW`, `REWORK`, `DONE`, `REJECTED`, `CANCELLED` |
| `submission_type` | `REVIEW`, `BLOCKED`, `CHANGE_REQUEST` |
| Validation result | `PASS`, `FAIL`, `SKIPPED` |
| Change decision | `APPROVE_CHANGE`, `REJECT_CHANGE`, `REQUEST_INFO` |

A submission type is not a task status. Only Lord updates authoritative task outcomes.

## Core Workflow

1. Lord selects the project structure and task profile.
2. Lord assigns a task ID such as `Task-A-01` and writes the task package.
3. Lord defines boundaries, dependencies, outputs, acceptance IDs, validation methods, runtime, and `submission_path`.
4. Lord dispatches a Serf executor using a short instruction that points to the task package.
5. Serf executes only the assigned work and submits `REVIEW`, `BLOCKED`, or `CHANGE_REQUEST`.
6. Lord reviews actual outputs and evidence, then updates the authoritative state source.

## Coordination Patterns

| Pattern | Use when | Reference |
|---|---|---|
| Sequential | Work is dependent, or one executor is enough | `lord/references/dispatch-modes.md` |
| Intra-application division of labor | Several workers run in one application on disjoint paths | `lord/references/intra-app-parallelism.md` |
| Cross-application handoff | The executor runs in another application without shared chat | `lord/references/cross-application-handoff.md` |

Both patterns keep one protocol: one task package per worker, one `submission_path` per task, and Lord as the only writer of the authoritative state source. `handoff` and `host` are optional dispatch instruction fields, and Serf reports `execution_host` when it is known.

```
handoff: dsh → word        (task package travels unchanged)
fan-out: dsh → serf A, serf B, serf C   (disjoint paths, one wave)
```

## Common Fields

Task packages use these shared fields:

```yaml
protocol_version: "0.6"
profile:  # micro | standard | full
project_id:
task_id:
task_version:
updated_at:
task_status:
objective:
inputs: []
allowed_paths: []
forbidden_paths: []
expected_outputs: []
acceptance_criteria: {}
validation_methods: []
depends_on: []
inherits: []
execution_environment:
  requires_python: false
submission_path:
```

`standard` and `full` task packages add these fields; `output_language` is optional:

```yaml
target_adapter:  # generic-chat | coding | document | api | shared-workspace
dispatch_mode:  # direct | semi-automatic | manual-copy
authoritative_state_source:  # e.g. PROJECT_PLAN.md
output_language:
```

Serf submissions share this envelope:

```yaml
protocol_version: "0.6"
profile:
project_id:
task_id:
executed_task_version:
submitted_at:
submission_type: REVIEW  # REVIEW | BLOCKED | CHANGE_REQUEST
task_package_path:
report_path:
```

## Canonical Submission Assets

```text
serf/assets/templates/micro-review-report.yaml
serf/assets/templates/review-report.md
serf/assets/templates/blocker-report.md
serf/assets/templates/change-request-report.md
serf/assets/schemas/submission-envelope.schema.yaml
serf/assets/schemas/micro-review-report.schema.yaml
serf/assets/schemas/review-report.schema.yaml
```

## Report Paths and Commands

```text
micro REVIEW:             REVIEWS/Task-A-01-REVIEW.yaml
standard/full REVIEW:     REVIEWS/Task-A-01-REVIEW.md
BLOCKED:                  BLOCKERS/Task-A-01-BLOCKER.md
CHANGE_REQUEST:           CHANGE_REQUESTS/Task-A-01-CHANGE-REQUEST.md
```

```text
$lord review REVIEWS/Task-A-01-REVIEW.yaml
$lord review REVIEWS/Task-A-01-REVIEW.md
$lord resolve BLOCKERS/Task-A-01-BLOCKER.md
$lord resolve CHANGE_REQUESTS/Task-A-01-CHANGE-REQUEST.md
```

## Runtime and Language

For Python work, Lord specifies a conda environment path, exact Python executable, or activation command. Serf uses that runtime and reports `BLOCKED` if it is unavailable.

Output language defaults to the active conversation language. The skills include guidance for UTF-8, CJK text, localized paths, shell quoting, Unicode-aware checks, and rendering-width hazards.

On DSH the executor runs a DeepSeek model. Write those task packages with numbered, checkable steps and exact paths; the same rules are recorded in `lord/references/host-runtimes.md` and `serf/references/host-runtimes.md`.

## Validation

```text
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
```

The validator checks UTF-8/LF hygiene, skill and UI metadata, canonical vocabulary, local references, YAML and JSON Schema definitions, template/profile compatibility, template heading structure, reference indexing, host and handoff assets, and representative protocol payloads. GitHub Actions runs the same command on pushes and pull requests.

If Codex's `skill-creator` validator is available on Windows, force UTF-8 first:

```powershell
$env:PYTHONUTF8 = "1"
python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ".\lord"
python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ".\serf"
```

## Migrating to Protocol 0.6

Regenerate unfinished task packages, dispatch instructions, and reports with `protocol_version: "0.6"`. Field names did not change from 0.5, so the mechanical edit is the version constant; 0.6 adds the optional `host` and `handoff` dispatch blocks and the optional `execution_host` report field.

Protocol 0.6 keeps the compact project context index added in 0.5 and still rejects deprecated v0.3 field names in submission envelopes.

For Protocol 0.3 users, 0.6 retains the canonical names introduced in 0.4:

| v0.3 | v0.6 |
|---|---|
| `agent_id`, `Agent-A-01` | `task_id`, `Task-A-01` |
| `status` | `task_status` |
| `target_agent_type` | `target_adapter` |
| `required_files` | `inputs` |
| `allowed_changes` | `allowed_paths` |
| `return_path`, `handoff_path` | `submission_path` |
| `acceptance` | `acceptance_criteria` |
| Task `validation` | `validation_methods` |
| Submission `changed`, `result`, `validation` | `changed_outputs`, `results`, `validation_results` |
| `HANDOFFS/` | `REVIEWS/` |
| `agent-task.md` | `task-package.md` |
| `micro-handoff.yaml`, `review-handoff.md` | `micro-review-report.yaml`, `review-report.md` |

The `$lord` command belongs to the chat/transport layer and is not stored as `lord_invocation` in machine-readable reports. Finish active older-protocol work before upgrading, or regenerate unfinished task packages and reports as v0.6.

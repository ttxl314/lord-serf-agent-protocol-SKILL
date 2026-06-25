# Project Scaling and Task Profiles

## 1. Principle

Use the smallest file structure and the smallest task package that can support the current work safely. Do not force a full governance system or full task template onto a simple project.

Do not generate empty sections. Do not repeat stable project context in every task. Prefer references to authoritative files.

## 2. Small Projects

Use when:

- There are 1 to 5 tasks.
- There is one main deliverable.
- There are few modules and simple interfaces.
- The collaboration cycle is short.

Recommended structure:

```text
PROJECT.md
TASKS.md
HANDOFFS/
```

`TASKS.md` is the single authoritative source for task status.

## 3. Medium Projects

Use when:

- There are 6 to 20 tasks.
- Multiple related modules are involved.
- Explicit dependencies exist.
- Multiple external agents need to collaborate.

Recommended structure:

```text
PROJECT_OVERVIEW.md
PROJECT_PLAN.md
ARCHITECTURE.md
TASKS/
DISPATCH/
HANDOFFS/
ISSUES.md
```

`PROJECT_PLAN.md` is the single authoritative source for task status.

## 4. Large Projects

Use when:

- There are more than 20 tasks.
- Work spans multiple tools, teams, or a long-running collaboration.
- Complex interfaces, versions, or change control are required.
- Machine-readable state is needed.

Recommended structure:

```text
PROJECT_OVERVIEW.md
PROJECT_PLAN.md
TASK_REGISTRY.yaml
ARCHITECTURE.md
INTERFACES.md
DECISIONS.md
ISSUES.md
CHANGELOG.md
TASKS/
DISPATCH/
HANDOFFS/
BLOCKERS/
CHANGE_REQUESTS/
OUTPUTS/
```

`TASK_REGISTRY.yaml` is the machine-readable authoritative state source. `PROJECT_PLAN.md` is the human-readable planning view.

## 5. Task Profiles

Project scale and task profile are separate decisions. A large project may still contain many `micro` tasks.

### Micro

Use when all are true:

- One clear objective.
- No more than 2 changed files, unless the files are trivial and tightly related.
- No public interface, architecture, shared data structure, or shared-path change.
- No complex dependency or overlapping file ownership.
- No more than 3 acceptance criteria.
- Low-risk and easy to reverse.

Use `assets/templates/micro-task.yaml`.

Target size:

- Task package: about 100-250 English words or 200-500 Chinese characters.
- Handoff: about 80-180 English words or 150-350 Chinese characters.

### Standard

Use for ordinary module-level work that involves several related files, simple dependencies, routine design judgment, or build/test validation.

Use `assets/templates/agent-task.md`, but omit sections that do not apply.

### Full

Use when any are true:

- Public interface or architecture changes.
- Shared schema, database, configuration, or data-structure changes.
- Multi-agent coordination or complex dependencies.
- High-risk, security-sensitive, or difficult-to-reverse work.
- Detailed rollback, approval, or recovery evidence is required.

Use the full task and handoff templates.

## 6. Context Economy Rules

- Do not repeat project defaults such as runtime, language, encoding, or package policy when they are already defined in an authoritative project file.
- Inherit stable defaults by file reference.
- Keep launch instructions to a task-file reference and essential execution note.
- Use acceptance criterion IDs instead of copying criterion text into handoffs.
- Use delta instructions for rework.
- Detailed reports may grow with task complexity; human-facing notifications should not.
- If a low-risk task package is longer than the work description and acceptance evidence combined, simplify it before dispatch.

## 7. Upgrade Conditions

Upgrade the project structure when:

- The number of tasks grows materially.
- Multiple agents work at the same time.
- Status, interface, or file conflicts become frequent.
- The project needs automatic filtering of ready tasks.
- Cross-session recovery becomes noticeably expensive.

Upgrade a task profile only when risk, dependency complexity, shared interfaces, file ownership, or validation requirements justify it.

# Project Scaling

## 1. Principle

Use the smallest file structure that can support the current project. Do not force a full governance system onto a simple project.

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

## 5. Upgrade Conditions

Upgrade the project structure when:

- The number of tasks grows materially.
- Multiple agents work at the same time.
- Status, interface, or file conflicts become frequent.
- The project needs automatic filtering of ready tasks.
- Cross-session recovery becomes noticeably expensive.

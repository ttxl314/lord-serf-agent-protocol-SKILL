# Task Status and Dependencies

## 1. Status Definitions

- `PENDING`: Created, but prerequisites are not satisfied.
- `READY`: Dependencies are satisfied and the task can be dispatched.
- `IN_PROGRESS`: An external agent is executing the task.
- `BLOCKED`: Required input, dependency, or decision is missing.
- `REVIEW`: Output has been returned and awaits master-agent review.
- `REWORK`: Review failed and revision is required.
- `DONE`: Accepted by the master agent.
- `REJECTED`: Output or approach was rejected.
- `CANCELLED`: Cancelled because the project changed.

## 2. Normal Flow

`PENDING → READY → IN_PROGRESS → REVIEW → DONE`

Common exception flows:

- `IN_PROGRESS → BLOCKED`
- `REVIEW → REWORK`
- `REWORK → IN_PROGRESS`
- `REVIEW → REJECTED`
- `PENDING/READY → CANCELLED`

## 3. Authoritative State Source

- Small projects: `TASKS.md`
- Medium projects: `PROJECT_PLAN.md`
- Large projects: `TASK_REGISTRY.yaml`

Statuses in task files, handoff files, and chat history are descriptive only. They do not override the authoritative state source.

External agents may submit only `REVIEW`, `BLOCKED`, or a change request. `DONE`, `REJECTED`, and `CANCELLED` may only be written to the authoritative state source by the master agent after review or decision.

## 4. Dependency Checks

Before a task enters `READY`, confirm that:

- Required files exist.
- Upstream tasks have reached the required status.
- Upstream handoffs are readable.
- Public interfaces are defined.
- Input data is complete.
- The task version is current.

## 5. Parallel Execution Conditions

Allow parallel execution only when all conditions are true:

- Tasks do not modify the same controlled core files.
- Tasks do not depend on each other's unfinished outputs.
- Shared interfaces are frozen or explicit.
- Work boundaries do not overlap.
- The master agent has confirmed there is no conflict.

## 6. Blocker Handling

When a critical dependency is missing, move the task to `BLOCKED` and submit a blocker report.

For non-critical local issues, make reversible and documented assumptions instead of blocking unnecessarily.

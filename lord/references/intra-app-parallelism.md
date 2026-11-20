# Intra-Application Division of Labor

## 1. Two Shapes

- Sequential: one executor at a time; the default for dependent work.
- Fan-out: several executors inside one application, each holding one task package.

Fan-out is an execution choice. Task IDs, packages, and submission paths stay identical.

## 2. Fan-Out Preconditions

All must hold before the first worker starts:

- Allowed paths are disjoint across the wave.
- Shared interfaces are frozen or explicitly versioned.
- No task in the wave depends on an unfinished task in the same wave.
- Each task has its own `submission_path`.
- Lord has written the authoritative state source for every task in the wave.

If one precondition fails, split the wave or run it sequentially.

## 3. Worker Instantiation

Give each worker exactly:

- The Serf skill.
- One task package path.
- Its `submission_path`.
- The runtime note, when Python is required.

Do not give a worker the project plan, a second task package, or edit rights on the state source.

Prefer a worker that starts from the package alone: DSH `subagent` rather than `subagent_fork`, a Claude Code `Task` subagent without conversation history, a Codex subagent without inherited context. When the host only offers a forked context, name the task package path first and tell the worker to ignore remembered chat.

## 4. Single-Writer Rules

- One writer per path per wave.
- Lord is the only writer of the authoritative state source.
- A worker may not modify another worker's outputs, not even to fix them.
- Integration or merge work is its own task with its own package.

## 5. Concurrency

Start with the smallest wave that still shortens the critical path. Four concurrent workers is a safe default ceiling; raise it only while paths stay disjoint and reviews keep pace.

Review reports as they arrive. A wave does not need to finish before review starts.

## 6. Failure Isolation

- One `BLOCKED` worker does not stall the others.
- Reassignment means a new task version or a new task, never a silent rerun of the same version.
- A crashed or abandoned worker returns to `READY` only after Lord confirms which paths it touched.

## 7. Aggregation

- Review each report against its own package.
- Add one integration task when outputs interact, with one acceptance criterion per interaction.
- Declare the wave done only when every task is `DONE` and the integration check passes.

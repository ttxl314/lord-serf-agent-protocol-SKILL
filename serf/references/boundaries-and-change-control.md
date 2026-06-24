# Boundaries and Change Control

## 1. Work Boundary

Stay inside the task's declared responsibility. Do not take over upstream, downstream, planning, registry, or acceptance work unless the task explicitly assigns it.

## 2. Allowed Local Judgment

Make local implementation decisions when they:

- Do not change public interfaces.
- Do not alter shared architecture or data structures.
- Do not affect other agents' tasks.
- Are reversible or easy for lord to review.
- Are documented in the handoff.

## 3. Change Request Required

Submit a change request before changing:

- Public APIs, function signatures, schemas, or data contracts.
- Shared configuration, paths, or build behavior.
- Module boundaries or architecture.
- Outputs assigned to another agent.
- Accepted prior work.
- The task's acceptance criteria or validation plan.

## 4. Forbidden Actions

Do not:

- Modify forbidden controlled files.
- Claim a dependency is satisfied without evidence.
- Suppress errors to make validation appear successful.
- Edit task status to `DONE`.
- Use broad refactors as a substitute for the assigned task.

# Dispatch Modes

## 1. Direct

Use `direct` when the current environment can start the target Serf executor through a verified API, connector, or automation.

- Write the task package before invocation.
- Record the target adapter, task ID, task version, dispatch time, and invocation result.
- Claim execution started only after invocation succeeds.
- Never use a platform-temporary ID as the only project or task identifier.

## 2. Semi-Automatic

Use `semi-automatic` when the current environment can prepare all artifacts but a user must perform one launch or transfer action.

Provide only:

- Task-package path.
- Serf launch instruction.
- Required unavailable inputs.
- Essential runtime note.
- Expected submission path.

Do not claim execution started until the user or platform confirms it.

## 3. Manual Copy

Use `manual-copy` when another independent session has no shared workspace or direct connector.

Transfer only:

- The task package.
- Required inputs not otherwise accessible.
- The matching Serf submission template.
- A short instruction to save the report at `submission_path`.

## 4. Selection Rule

Choose the most direct mode that the current environment can verify. A dispatch instruction never redefines goals, boundaries, acceptance criteria, validation methods, or runtime; those belong to the task package.

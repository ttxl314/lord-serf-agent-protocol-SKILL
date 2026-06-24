# Dispatch Modes

## 1. Direct Dispatch

Use when:

- The current environment has an API, connector, or automation capability for the target agent.
- The task body or file references can be transmitted.
- Structured return results can be received.

Requirements:

- Preserve project ID, task ID, and task version.
- Record dispatch time and target.
- Require structured return data.
- Do not use a platform-internal temporary ID as the only project identifier.
- Claim that the external agent has started only after the actual invocation succeeds.

## 2. Semi-Automatic Dispatch

Use when:

- The current environment can create files but cannot directly invoke the target software.

Output:

- Formal task file.
- Required file list.
- Target agent launch instruction.
- Suggested save paths.
- Return handoff requirements.
- A clear note that the user or target environment must perform the actual launch.

## 3. Manual Copy

Use when:

- Only text can be copied or a small number of files can be uploaded.

Requirements:

- Generate a self-contained launch instruction.
- Clearly list files the user must upload.
- Avoid relying on shared directories.
- Require the external agent to return a complete handoff report.
- Do not claim the external task was started automatically.

## 4. Mode Selection

Prefer the strongest verifiable mode. If capability is unclear, default to manual copy.

Launch instructions must not redefine task goals, boundaries, or acceptance criteria. Those belong to the formal task file.

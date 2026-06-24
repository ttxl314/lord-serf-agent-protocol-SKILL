# Coding Agent Adapter

Use for development agents that can read a code repository, modify files, and run commands.

## Add to the Task Package

- Repository or workspace root.
- Branch, worktree, or isolated workspace rules.
- Editable paths.
- Forbidden paths.
- Build, test, and static-check commands.
- Dependency installation limits.
- Python runtime requirements when Python is needed: `conda_env_path`, `python_executable`, or `activation_command`.
- Expected generated files.
- Rollback requirements.

## Add to the Handoff

- File-level change list.
- Key implementation notes.
- Commands actually executed.
- Runtime actually used, including conda environment path or Python executable for Python work.
- Test, build, and check results.
- Validations not run and reasons.
- Interface changes.
- Potential compatibility risks.

Do not allow multiple parallel agents to modify the same core file unless the master agent has defined a merge strategy.

For Python tasks, lord must specify the conda environment path or exact Python executable whenever the external agent may need to run scripts, tests, notebooks, or Python-based tooling. If the environment is unknown, assign a discovery step explicitly or require the external agent to return a blocker instead of guessing.

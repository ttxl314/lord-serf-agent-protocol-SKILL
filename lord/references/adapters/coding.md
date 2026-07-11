# Coding Adapter

## Task Package

- Name repository root, allowed paths, forbidden paths, and expected changed outputs.
- Identify public interfaces, generated files, migrations, and shared configuration.
- Specify exact build, lint, test, type-check, and security commands that matter to acceptance.
- Define the required runtime and package-install policy.

## Submission Report

- List changed outputs, not every file read.
- Map validation results to stable acceptance IDs.
- Record skipped checks, runtime differences, assumptions, issues, and interface impact.
- Keep logs concise and point to saved artifacts when available.

## Parallel Safety

Do not assign overlapping controlled paths to parallel Serf executors unless Lord defines ownership and a merge strategy.

For Python tasks, Lord must specify a conda environment path, exact Python executable, or activation command. If the runtime is unknown, assign discovery explicitly or require `BLOCKED`.

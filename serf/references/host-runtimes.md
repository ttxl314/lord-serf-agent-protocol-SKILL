# Host Runtimes

## 1. Detect the Host

Before work, identify how you were started and record it as `execution_host`:

| Host | Invocation | Report delivery |
|---|---|---|
| Claude Code | `/serf` or automatic by description | file; a write may need approval |
| Codex | `$serf` | file; the sandbox decides which paths |
| DSH (DeepSeek) | `skill("serf")`, often through `subagent` | file inside the workspace, else inline |
| Generic chat | attached `SKILL.md` | inline only |

When you cannot write the report, use the compact inline YAML from `references/submission-reporting.md` and say so in the first line.

## 2. Nothing Else Changes

Host differences never change field names, status values, submission types, adapter names, paths, or report structure. When a host instruction contradicts the task package, follow the task package and record the conflict; if the conflict changes scope, submit `BLOCKED`.

## 3. Host Limits

- Claude Code: a write can wait on approval. A denied or unanswered prompt is a blocker, not permission to skip the file.
- Codex: the sandbox decides which paths are writable. Do not retry a denied write outside `allowed_paths`.
- DSH: writes are limited to the workspace root. A `submission_path` outside it becomes an inline report.

## 4. DeepSeek Executor Profile

When you run on DSH with DeepSeek models, apply these habits:

- Read the task package and its indexed files before writing anything.
- Follow the task's numbered steps in order: `execution_steps` for `standard` or `full`; for `micro`, the `objective` and the order of `expected_outputs`. Do not merge, reorder, or extend them.
- Verify every claim with a command, a file read, or an artifact before reporting it.
- Prefer exact commands and paths over prose.
- Keep the report literal: results, changed outputs, acceptance evidence.
- When a step is ambiguous or an input is missing, submit `BLOCKED` instead of assuming.
- On resume, re-read the package; never rely on remembered context.

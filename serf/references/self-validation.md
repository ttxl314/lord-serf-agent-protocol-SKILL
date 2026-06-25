# Self-Validation

## 1. Validation Standard

Validate actual outputs against acceptance IDs. Prefer checks Lord can inspect or reproduce.

Use task-defined methods first. Add a local check only when it materially reduces risk and stays inside scope.

## 2. Evidence Economy

Record concise evidence:

- Command or tool and the meaningful result.
- Artifact or file inspected.
- Manual check performed.
- Skipped check and reason.
- Validation limitation.

Do not paste full successful logs. One check may support multiple acceptance IDs; reference it once.

## 3. Rework

For a delta-only REWORK, rerun failed or affected acceptance IDs and only the regression checks required by their dependencies. Do not mechanically rerun every previously successful check.

## 4. Code Work

Use the project's normal tests, build, lint, or static checks when available. If a command cannot run, record the exact missing dependency, runtime, permission, or other blocker.

For Python work, record the actual conda environment or executable, invocation command, and Python version when relevant. Do not silently validate with a different interpreter.

## 5. Document or Content Work

Verify required output completeness, format, terminology, citations, filenames, and identified human-review points. Do not produce a second narrative summary when the artifact and acceptance evidence already show the result.

## 6. CJK and Localized Text

When relevant, check UTF-8 encoding, full-width punctuation, invisible spaces, non-ASCII paths, shell quoting, Unicode-aware matching, and rendering width.

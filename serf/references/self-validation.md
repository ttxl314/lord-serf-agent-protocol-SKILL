# Self-Validation

## 1. Validation Standard

Validate the actual output, not the intended plan. Prefer checks that lord can reproduce.

Use the validation methods specified in the task package first. Add reasonable local checks when they reduce risk and stay within scope.

## 2. Evidence to Capture

Record:

- Commands or tools run.
- Test, build, lint, render, compile, or inspection results.
- Files or artifacts inspected.
- Manual checks performed.
- Checks skipped and why.
- Known limitations of validation.

## 3. Code Work

For code tasks, validate with the project's normal commands when available. If commands cannot be run, explain the exact blocker, such as missing dependency, unavailable environment, permission issue, or time limit.

For Python tasks, record the actual runtime used:

- conda environment path or name
- Python executable path
- `python --version` result when available
- activation or invocation command used

Run validation with the specified runtime from the task package. Do not validate with a different interpreter unless the handoff clearly marks that limitation.

## 4. Document or Content Work

For document, design, or content tasks, verify output completeness, formatting requirements, terminology, citations, filenames, and any required review notes.

## 5. CJK and Localized Text

When Chinese or other CJK text is involved, check UTF-8 encoding, full-width punctuation, invisible spaces, non-ASCII paths, shell quoting, Unicode-aware length or regex behavior, and rendering width where relevant.

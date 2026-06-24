# Reporting

## 1. REVIEW Handoff

Use `assets/templates/review-handoff.md` when the assigned task is ready for lord's review. The status must be `REVIEW`, not `DONE`.

The handoff must include enough evidence for lord to inspect or reproduce the result:

- Task version executed.
- Files actually read.
- Added or modified files.
- Completed work.
- Validation performed.
- Actual validation results.
- Assumptions, risks, and incomplete items.
- Any downstream notes.

## 2. Blocker Report

Use `assets/templates/blocker-report.md` when execution cannot continue because input, permissions, dependencies, decisions, or task clarity are missing.

Blocker reports should be precise and actionable. Include what was attempted and what lord must decide or provide.

## 3. Change Request

Use `assets/templates/change-request.md` when success requires changing boundaries, public interfaces, architecture, shared paths, shared data structures, or another task's scope.

Do not implement the requested change unless lord approves or the original task package explicitly delegated that authority.

## 4. Output Completeness

If the platform cannot create files directly, return the complete report content in the conversation so the user can paste it into the requested path.

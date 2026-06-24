# Review and Acceptance

## 1. Review Inputs

The master agent should read:

- Current task file.
- Relevant task version.
- External agent handoff report.
- Files actually added or modified.
- Validation commands and actual results.
- Related interfaces and upstream outputs.

## 2. Required Checks

1. Task ID and project ID match.
2. The output is based on the latest task version.
3. All expected outputs are complete.
4. No forbidden controlled files were modified.
5. Architecture and interface constraints are respected.
6. Validation results can be reproduced or reviewed.
7. No undeclared interface or data-structure changes were introduced.
8. Downstream task impact is understood.
9. The handoff accurately describes the actual output.

## 3. Review Outcomes

### PASS

All critical checks pass. The master agent updates the authoritative status to `DONE`.

### REWORK

The direction is acceptable, but fixable issues remain. The master agent must list:

- Failed checks.
- Required fixes.
- Things that must not be changed.
- New submission requirements.
- Whether the task version changes.

### REJECTED

The output seriously diverges from the task, violates architecture, or is no longer applicable. Preserve the record and create replacement tasks if needed.

## 4. Trust Boundary for External Outputs

Do not accept work merely because the handoff claims tests passed. When possible, read actual files or rerun validation. If validation cannot be reproduced, record the limitation clearly.

An external agent's `REVIEW` means "ready for review," not complete. Only the master agent may move the task to `DONE` after the checks above.

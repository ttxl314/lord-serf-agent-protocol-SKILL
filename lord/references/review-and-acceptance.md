# Review and Acceptance

## 1. Review Inputs

Read the current task version, the Serf report, actual changed outputs, acceptance evidence, and only the interfaces or upstream artifacts relevant to the change. Do not reload unrelated project context.

## 2. Required Checks

1. IDs, protocol version, and executed task version match.
2. Expected outputs are present.
3. Changed files stay inside the allowed boundary.
4. Acceptance evidence maps to the declared acceptance IDs.
5. No undeclared interface, schema, architecture, shared-path, or downstream-impact change was introduced.
6. The report accurately describes the actual output.

## 3. Evidence Reuse and Review Depth

Do not automatically repeat all Serf validation.

- Micro: inspect the change or artifact and review Serf evidence; do not rerun the same checks by default.
- Standard: reproduce only uncertain, high-value, or representative checks.
- Full: reproduce critical high-risk checks, especially interface, security, migration, irreversible, or shared-schema behavior.

Increase revalidation when evidence is missing, failed, skipped, contradictory, produced under a different runtime, or the output cannot be inspected directly. Also increase it when the user explicitly requests full reproduction.

One command or artifact may satisfy multiple acceptance IDs. Reuse the evidence reference instead of repeating the command or log.

## 4. Outcomes

### PASS

All critical checks pass. Lord updates the authoritative status to `DONE`.

### REWORK

Return delta-only instructions:

- Failed or affected acceptance IDs.
- Required changes.
- Outputs or interfaces that must be preserved.
- Acceptance IDs that must be revalidated.
- Whether the task version changes.

Do not restate the full task. Serf revalidates failed or affected criteria plus only the regression checks required by their dependencies.

### REJECTED

The output materially diverges from the task, violates architecture or boundaries, or is no longer applicable. Preserve the record and create replacement work when needed.

## 5. Trust Boundary

Do not accept a claim merely because a report says it passed. Review actual outputs and evidence at the risk-appropriate depth above. A Serf `REVIEW` means ready for Lord review, not complete.

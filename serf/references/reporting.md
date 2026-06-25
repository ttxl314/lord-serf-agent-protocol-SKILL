# Reporting

## 0. Final Response Gate

Before sending any final response for a completed task, blocker, or change request, verify that the response contains all of these sections:

1. `# Human Summary`
2. The full handoff, blocker report, or change request content
3. A separate lord invocation section
4. A fenced command block whose first line is `$lord`, unless the target platform does not support `$lord`

If any item is missing, do not send the final response yet. Add the missing section first.

Keep `# Human Summary` concise: 1-3 short lines or at most 3 bullets. Do not duplicate the full report there.

## 1. REVIEW Handoff

Use `assets/templates/review-handoff.md` when the assigned task is ready for lord's review. The status must be `REVIEW`, not `DONE`.

Start the final response with a very brief human-readable summary. Keep it to 1-3 short lines or at most 3 bullets: what was done, what was validated, and what lord should review.

The handoff must include enough evidence for lord to inspect or reproduce the result:

- Task version executed.
- Files actually read.
- Added or modified files.
- Completed work.
- Validation performed.
- Actual validation results.
- Assumptions, risks, and incomplete items.
- Any downstream notes.

After the handoff, include a separate copyable lord invocation command. It should start with `$lord` when the platform supports skill-style invocation and should ask lord to review the exact returned report or handoff path.

## 2. Blocker Report

Use `assets/templates/blocker-report.md` when execution cannot continue because input, permissions, dependencies, decisions, or task clarity are missing.

Blocker reports should be precise and actionable. Include what was attempted and what lord must decide or provide.

After a blocker report, include a separate `$lord` invocation command asking lord to resolve the blocker or update the task package.

## 3. Change Request

Use `assets/templates/change-request.md` when success requires changing boundaries, public interfaces, architecture, shared paths, shared data structures, or another task's scope.

Do not implement the requested change unless lord approves or the original task package explicitly delegated that authority.

After a change request, include a separate `$lord` invocation command asking lord to approve, reject, or revise the requested change.

## 4. Output Completeness

If the platform cannot create files directly, return the complete report content in the conversation so the user can paste it into the requested path.

## 5. Lord Invocation Format

Use this shape for the copyable command:

```text
$lord
Review the returned serf report for project_id: [project_id], agent_id: [agent_id], executed_task_version: [executed_task_version].
Use the attached or pasted handoff/blocker/change-request content as the review input.
Do not mark DONE unless the actual outputs satisfy the task package acceptance criteria.
```

If `$lord` is unsupported on the target platform, replace the first line with: `Use the lord protocol to review this serf report.`

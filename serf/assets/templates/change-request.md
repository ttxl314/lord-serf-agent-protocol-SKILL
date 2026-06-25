---
project_id:
agent_id:
task_version:
requested_at:
change_status: PROPOSED
task_package_path:
---

# Human Summary

1-3 short lines or at most 3 bullets: the requested change, why it is needed, and whether it blocks execution.

# Change Request

## 1. Change Target

## 2. Reason for Change

## 3. Current Limitation

## 4. Proposed Approach

## 5. Alternatives

## 6. Affected Files

## 7. Affected Tasks

## 8. Validation and Rollback Plan

## 9. Whether This Blocks the Current Task

## 10. Requested Lord Decision

Lord should answer with `APPROVED`, `REJECTED`, or `NEEDS_INFO`.

# Lord Change-Request Invocation

```text
$lord
Review this serf change request for project_id: [project_id], agent_id: [agent_id], task_version: [task_version].
Approve, reject, or revise the requested change before serf continues.
```

# Cross-Application Handoff

## 1. When It Applies

Use this reference when one project spans applications that cannot see each other's chat. Example: DSH plans and reviews, a document editor produces the deliverable, and an IDE changes code.

Cross-application work is still one protocol. Only the transport changes.

## 2. Application Slots

Record every application that touches the project:

| Slot | Record |
|---|---|
| Application | Human name, for example `Word`, `Cursor`, `DSH` |
| Target adapter | One of the five canonical adapters |
| Skills | `lord`, `serf`, or neither |
| Workspace root | Path visible inside that application |
| Invocation | Exact form the application supports |
| Write access | Paths it can create or modify |
| Transport | How files leave and enter the application |

An application with no Serf skill is still usable: attach `SKILL.md` and keep the literal fields.

## 3. Transport Ladder

Choose the highest rung both applications share:

1. Shared workspace root: both sides read and write the same paths.
2. Synced or mounted folder: same paths, delayed visibility.
3. Upload and download: explicit transfer of named files.
4. Paste: inline YAML in chat, last resort.

Record the rung in `handoff.transport`. Never assume a file arrived; require the receiver to quote the `task_id` and `task_version` it actually read.

## 4. Handoff Artifact

Each hop carries one dispatch instruction with:

```yaml
handoff:
  from_app: dsh
  to_app: word
  transport: upload
  return_transport: upload
```

The task package does not fork. The same `task_id`, `task_version`, acceptance IDs, and `submission_path` travel unchanged.

## 5. Continuity Rules

- Task identity and version are immutable across hops. A new application starts a new execution of the same version, not a new task.
- Only the role holding Lord writes the authoritative state source. An application without write access returns the report, and Lord transcribes the status.
- The receiver quotes `task_id` and `task_version` in its first line back. Silence is not confirmation.
- Chat stays a notification; the report is the handoff.

## 6. Failure Modes

| Symptom | Action |
|---|---|
| Receiver cannot open the task package | `BLOCKED`, reason `handoff` |
| Receiver cannot write `submission_path` | Inline YAML report with `report_path: inline`; Lord transcribes before acceptance |
| Two applications return a report for one version | The file at `submission_path` is the latest run; accept the latest `submitted_at` and record the other as superseded |
| Version mismatch on arrival | Re-send the current package; never let the receiver upgrade or downgrade it |
